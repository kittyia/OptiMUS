import json
import gurobipy as gp
from gurobipy import Model, GRB

# Read inputs from JSON file
with open("data.json", "r") as f:
    inputs = json.load(f)

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
