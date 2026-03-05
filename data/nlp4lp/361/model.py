import json
import gurobipy as gp
from gurobipy import Model, GRB
import numpy as np


def generate_data(
    seed: int = 0,
    L: int = 5,
    K: int = 3,
    T: int | None = None,
    max_orders_per_period: int = 5,
    max_pool_size: int = 1000,
    max_fulfillment_orders: int = 1000,
    cost_scale: float = 1.0,
):
    """Generate synthetic data that is guaranteed to be feasible with the
    current optimization model (without changing the model).

    Parameters
    - seed: random seed
    - L: maximum stay in the pool (int)
    - K: number of probability groups (int)
    - T: last period (int). If None, defaults to (L+1)+10
    - max_orders_per_period: cap on arrivals per period (int)
    - max_pool_size: pool capacity per period (int)
    - max_fulfillment_orders: max flow per period (int)
    - cost_scale: scale for c_F coefficients (float)

    Returns a data dictionary with string time keys to match model access.
    """

    np.random.seed(seed)

    # Compute dependent dimensions
    t = L + 1
    if T is None:
        T = t + 10

    # Basic validation & safety adjustments
    if max_pool_size < max_orders_per_period * (L + 1):
        max_pool_size = max_orders_per_period * (L + 1)
    if max_fulfillment_orders < max_orders_per_period:
        max_fulfillment_orders = max_orders_per_period

    # Multiorder group probabilities (small, non-negative)
    p = [float(x) * 0.2 for x in np.random.rand(K).tolist()]

    # Orders arriving in each period (modest random arrivals)
    I = {
        str(tau): int(np.random.randint(0, max_orders_per_period + 1))
        for tau in range(t, T + 1)
    }

    # Set I_prime to zeros (no forced existing pool content)
    I_prime = {str(tau): [0 for _ in range(K)] for tau in range(t, T + 1)}

    # Set epsilon to zeros so no unexpected 'hits' reduce S_prime
    epsilon = {
        str(tau): {
            str(s): [0 for _ in range(K)] for s in range(max(t - L, tau - L), tau + 1)
        }
        for tau in range(t, T + 1)
    }

    # Provide a benign initial O (all zeros)
    O = {
        str(tau): {
            str(s): [0 for _ in range(K)] for s in range(max(t - L, tau - L), tau)
        }
        for tau in range(t, T + 1)
    }

    # Pool size and max flow
    C = {str(tau): int(max_pool_size) for tau in range(t, T + 1)}
    F_bar = {str(tau): int(max_fulfillment_orders) for tau in range(t, T + 1)}

    # Small per-period penalty coefficients
    c_F = {
        str(tau): float(0.1 * np.random.rand() * cost_scale) for tau in range(t, T + 1)
    }

    data = {
        "I": I,
        "I_prime": I_prime,
        "epsilon": epsilon,
        "O": O,
        "C": C,
        "F_bar": F_bar,
        "p": p,
        "c_F": c_F,
        "T": T,
        "L": L,
        "K": K,
        "t": t,
    }

    # Save a copy for inspection
    try:
        with open("data.json", "w") as f:
            json.dump(data, f, indent=4)
    except Exception:
        pass

    return data


inputs = generate_data()

I = inputs["I"]
I_prime = inputs["I_prime"]
epsilon = inputs["epsilon"]
O = inputs["O"]
C = inputs["C"]
F_bar = inputs["F_bar"]
p = inputs["p"]
c_F = inputs["c_F"]
T = inputs["T"]
t = inputs["t"]
L = inputs["L"]
K = inputs["K"]

# Create a new model
model = Model("OrderConsolidation")

# Decision variables
O = model.addVars(T + 1, T + 1, K, vtype=GRB.CONTINUOUS, name="O")
S = model.addVars(T + 2, T + 2, K, vtype=GRB.CONTINUOUS, name="S")
S_prime = model.addVars(T + 1, T + 1, K, vtype=GRB.CONTINUOUS, name="S_prime")

# Objective function: Maximize multiorder hits
model.setObjective(
    gp.quicksum(
        p[k] * S[tau + 1, s, k]
        for tau in range(t, T + 1)
        for s in range(tau - L + 1, tau + 1)
        for k in range(K)
    )
    - gp.quicksum(
        c_F[str(tau)]
        * (
            gp.quicksum(O[tau, s, k] for s in range(tau - L, tau + 1) for k in range(K))
            - F_bar[str(tau)]
        )
        for tau in range(t, T + 1)
    ),
    GRB.MAXIMIZE,
)

# Constraints
for tau in range(t, T + 1):
    for k in range(K):
        # TODO: is it range(tau - L + 1, tau + 1) or range(tau - L, tau)
        for s in range(tau - L + 1, tau + 1):
            model.addConstr(
                S_prime[tau, s, k] == S[tau, s, k] - epsilon[str(tau)][str(s)][k]
            )
        model.addConstr(S_prime[tau, tau, k] == I_prime[str(tau)][k])
        # TODO: range(tau - L + 1, tau + 1) or range(tau - L, tau)
        for s in range(tau - L + 1, tau + 1):
            model.addConstr(S[tau + 1, s, k] == S_prime[tau, s, k] - O[tau, s, k])
        model.addConstr(O[tau, tau - L, k] == S_prime[tau, tau - L, k])

    model.addConstr(
        # TODO: is it range(tau - L + 1, tau + 1) or range(tau - L, tau)
        gp.quicksum(
            S[tau + 1, s, k] for s in range(tau - L + 1, tau + 1) for k in range(K)
        )
        <= C[str(tau)]
    )

for k in range(K):
    model.addConstr(S[T + 1, T + 1, k] == 0)

for tau1 in range(T + 1):
    for tau2 in range(T + 1):
        for k in range(K):
            model.addConstr(S[tau1, tau2, k] >= 0)
            model.addConstr(O[tau1, tau2, k] >= 0)

# Optimize the model
model.optimize()

# Extract results
if model.status == GRB.OPTIMAL:
    print(f"Obj: {model.objVal}")
    from pathlib import Path

    Path("obj.txt").write_text(str(model.objVal))
else:
    print("No optimal solution found.")
