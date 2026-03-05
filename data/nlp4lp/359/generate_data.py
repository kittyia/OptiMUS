import json
import heapq
import random


def generate_data(N=20, num_shortcuts=None, seed=0):
    """Generate a deterministic instance for the truck routing problem.

    Parameters
    ----------
    N : int
        Number of zone nodes (including start `s` and end `t`). Default is 20.
    num_shortcuts : int | None
        Number of shortcut offsets to add per node (offsets 2..). If None, a
        small default is chosen (min(3, max(0, N-2))). Setting to 0 produces
        no shortcuts.
    seed : int
        Random seed used for deterministic generation.

    Behavior
    --------
    - Builds a small directed physical graph (A_P) and assigns positive arc
      lengths deterministically.
    - If possible, marks a single physical arc as "too long" (added to `L`)
      and populates `L_e` with the T-arcs `(i,j)` whose shortest path uses
      that arc. The generator only selects a long arc that actually appears on
      some shortest path; if none exists, `L` is left empty to avoid infeasible
      direct-service constraints over empty sets.
    - Optionally creates small example forbidden patterns `F` (3-node) and
      `F_4` (4-node) only when the instance has enough nodes (3 and 4
      respectively). Auxiliary sets `B_delta`, `hat_B_delta`, `E_delta`, and
      `hat_E_delta` are filled conservatively to reduce the chance of
      infeasibility.
    - Computes shortest paths (gamma) between all nodes in V_T using Dijkstra.
    - The generator is deterministic (seeded). For larger or randomized
      instance generation, add feasibility checks or incremental constraint
      generation as needed.

    Returns
    -------
    params : dict
        Dictionary of generated instance data; includes a `generator_params`
        entry with the values used to create the instance (N, num_shortcuts,
        seed).
    """

    random.seed(seed)

    if num_shortcuts is None:
        # Keep a small number of shortcuts by default to limit density
        num_shortcuts = min(3, max(0, N - 2))

    # Number of zone nodes (these are the nodes the truck must visit)
    # Default N is 20 but can be changed when calling generate_data(N=...).
    nodes = list(range(N))

    # Depot / start and arrival nodes (must be part of V_T)
    s = 0
    t = N - 1

    # Build a simple directed physical graph (A_P) and assign arc lengths
    A_P = []
    ell_arc = {}

    # Create a directed ring (bidirectional) to ensure strong connectivity
    for i in range(N - 1):
        A_P.append((i, i + 1))
        A_P.append((i + 1, i))

    # Add a few extra shortcuts to make the shortest paths vary
    # Controlled by num_shortcuts (offsets 2 .. 2+num_shortcuts-1)
    for i in range(N):
        for k in range(2, 2 + num_shortcuts):
            A_P.append((i, (i + k) % N))

    # Assign deterministic positive lengths to arcs
    for u, v in A_P:
        ell_arc[(u, v)] = 10 + ((u * 7 + v * 3) % 50)  # values in [10, 59]

    # No excessively long physical arcs in this generator (avoid direct-service coupling).
    # All physical arcs keep their deterministic small lengths assigned above.

    # Undirected edges set (empty here for simplicity)
    E_P = []

    # Build adjacency list for shortest-path computation
    adj = {i: [] for i in nodes}
    for (u, v), w in ell_arc.items():
        adj[u].append((v, w))

    # Dijkstra that returns paths as sequences of physical arcs
    def shortest_paths_from(src):
        dist = {n: float("inf") for n in nodes}
        prev = {}
        dist[src] = 0
        pq = [(0, src)]
        while pq:
            d, u = heapq.heappop(pq)
            if d != dist[u]:
                continue
            for v, w in adj[u]:
                nd = d + w
                if nd < dist[v]:
                    dist[v] = nd
                    prev[v] = u
                    heapq.heappush(pq, (nd, v))
        # reconstruct paths
        paths = {}
        for dst in nodes:
            if dst == src:
                continue
            if dist[dst] == float("inf"):
                paths[dst] = []
            else:
                cur = dst
                path = []
                while cur != src:
                    p = prev[cur]
                    path.append((p, cur))
                    cur = p
                path.reverse()
                paths[dst] = path
        return dist, paths

    # Compute gamma (shortest paths) and the derived T-arc lengths ell
    gamma = {}
    ell = {i: {} for i in nodes}
    for i in nodes:
        _, paths = shortest_paths_from(i)
        for j in nodes:
            if i == j:
                continue
            path = paths.get(j, [])
            gamma[str((i, j))] = path
            ell[i][j] = sum(ell_arc[a] for a in path) if path else float("inf")

    # V_T is the set of nodes to be visited by the truck (including s and t)
    V_T = nodes

    # V_ij: mapping used to forbid certain transitions; keep empty (no extra
    # traffic restrictions) so the generator produces feasible instances.
    V_ij = {str((i, j)): [] for i in V_T for j in V_T if i != j}

    # Determine block sides (physical arcs) that are considered "too long"
    # for the achique system. Choose the longest arc that actually appears on
    # at least one shortest path; if none do, leave L empty to avoid an
    # infeasible 'direct service' constraint over an empty set.
    arcs_in_paths = set()
    for path in gamma.values():
        for arc in path:
            arcs_in_paths.add(arc)

    candidate_arcs = [a for a in ell_arc.keys() if a in arcs_in_paths]
    if candidate_arcs:
        max_arc = max(candidate_arcs, key=ell_arc.get)
        L = [max_arc]
        L_e = {str(tuple(max_arc)): []}
        for i in V_T:
            for j in V_T:
                if i == j:
                    continue
                path = gamma[str((i, j))]
                if path and max_arc in path:
                    L_e[str(tuple(max_arc))].append((i, j))
        # Sanity: if for some reason no T-arcs use this arc, clear L to avoid
        # creating a constraint over an empty summation (which would be 0 >= 1).
        if not L_e[str(tuple(max_arc))]:
            L = []
            L_e = {}
    else:
        L = []
        L_e = {}
    # Forbidden 3-node sequences (F) - only create if there are enough nodes.
    # Keep the set small to avoid creating infeasible instances.
    if len(V_T) >= 3:
        F = [(0, 1, 2)]
    else:
        F = []

    # Forbidden 4-node sequences for simplicity: add one example if possible.
    # To reduce risk of infeasibility (especially for small n and the MTZ-like
    # subtour formulation), keep the auxiliary sets small and conservative.
    if len(V_T) >= 4:
        F_4 = [(0, 1, 2, 3)]
        delta = F_4[0]
        B_delta = {str(tuple(delta)): [0]}
        hat_B_delta = {str(tuple(delta)): []}
        E_delta = {str(tuple(delta)): [3]}
        hat_E_delta = {str(tuple(delta)): []}
    else:
        F_4 = []
        B_delta = {}
        hat_B_delta = {}
        E_delta = {}
        hat_E_delta = {}

    # Pack parameters into a dict (also write to data.json for inspection)
    params = {
        "A_P": A_P,
        "E_P": E_P,
        "ell": ell,
        "F": F,
        "gamma": gamma,
        "s": s,
        "t": t,
        "V_T": V_T,
        "V_ij": V_ij,
        "L": L,
        "L_e": L_e,
        "F_4": F_4,
        "B_delta": B_delta,
        "hat_B_delta": hat_B_delta,
        "E_delta": E_delta,
        "hat_E_delta": hat_E_delta,
        "generator_params": {"N": N, "num_shortcuts": num_shortcuts, "seed": seed},
    }

    # Persist generated instance for debugging/inspection
    with open("data.json", "w") as f:
        json.dump(params, f, indent=2)

    return params


params = generate_data(N=20)
