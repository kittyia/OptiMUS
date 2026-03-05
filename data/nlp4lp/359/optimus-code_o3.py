import json
from ast import literal_eval
from gurobipy import *

# ------------------------------------------------------------
# 1. read data ------------------------------------------------
with open("data.json", "r") as f:
    data = json.load(f)

# ------------------------------------------------------------
# 2. basic sets and helpers ----------------------------------
V = data["V_T"]                  # list of nodes
s = data["s"]                    # start node
t = data["t"]                    # terminal node
n = len(V)

# ------------------------------------------------------------
# 3. build weight matrix of the complete digraph -------------
ell = data["ell"]                # nested dict with string keys

weights = {}                     # (i,j) -> distance
for key, path in data["gamma"].items():
    # key has format "(i, j)"
    i, j = literal_eval(key)
    # skip self-loops
    if i == j:
        continue
    # compute length of the shortest admissible path γ_(i,j)
    w = 0
    for u, v in path:
        w += ell[str(u)][str(v)]
    weights[(i, j)] = w

# ------------------------------------------------------------
# 4. build the model -----------------------------------------
model = Model()

# decision: x_ij = 1 if arc (i,j) is chosen in the tour
x = model.addVars(weights.keys(), vtype=GRB.BINARY, name="x")

# MTZ order variables: position of each node in the path
u = model.addVars(V, vtype=GRB.INTEGER, lb=0, ub=n - 1, name="pos")

# objective: minimise total travelled distance
model.setObjective(quicksum(weights[ij] * x[ij] for ij in weights), GRB.MINIMIZE)

# ------------------------------------------------------------
# 5. degree constraints --------------------------------------
for v in V:
    in_arcs  = [ (i, v) for i in V if (i, v) in weights ]
    out_arcs = [ (v, j) for j in V if (v, j) in weights ]

    if v == s:
        model.addConstr(quicksum(x[ij] for ij in in_arcs)  == 0, name=f"in_s")
        model.addConstr(quicksum(x[ij] for ij in out_arcs) == 1, name=f"out_s")
    elif v == t:
        model.addConstr(quicksum(x[ij] for ij in in_arcs)  == 1, name=f"in_t")
        model.addConstr(quicksum(x[ij] for ij in out_arcs) == 0, name=f"out_t")
    else:
        model.addConstr(quicksum(x[ij] for ij in in_arcs)  == 1, name=f"in_{v}")
        model.addConstr(quicksum(x[ij] for ij in out_arcs) == 1, name=f"out_{v}")

# ------------------------------------------------------------
# 6. MTZ subtour elimination (path version) ------------------
M = n  # sufficiently large
model.addConstr(u[s] == 0,     name="pos_start")
model.addConstr(u[t] == n-1,   name="pos_end")

for (i, j) in weights:
    if j == s or i == t:
        # arcs into s or out of t do not exist due to degree constraints
        continue
    # if arc (i,j) is used then pos_j = pos_i + 1
    model.addConstr(u[j] >= u[i] + 1 - M * (1 - x[(i, j)]), name=f"ord1_{i}_{j}")
    model.addConstr(u[j] <= u[i] + 1 + M * (1 - x[(i, j)]), name=f"ord2_{i}_{j}")

# ------------------------------------------------------------
# 7. solve ----------------------------------------------------
model.optimize()

# ------------------------------------------------------------
# 8. write solution ------------------------------------------
solution = {
    "variables": {var.VarName: int(round(var.X)) for var in model.getVars() if var.X > 1e-6},
    "objective": model.objVal
}

with open("solution.json", "w") as f:
    json.dump(solution, f, indent=4)
