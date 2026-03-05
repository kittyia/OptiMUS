import json
import gurobipy as gp
from gurobipy import GRB

# Load parameters from JSON file
with open("data.json", "r") as f:
    params = json.load(f)

S = params["S"]
C = params["C"]
C_t = params["C_t"]
A = params["A"]
c = params["c"]
E = params["E"]
G = params["G"]
T = params["T"]
lambda_param = params["lambda"]
mu = params["mu"]

# Create a new model
model = gp.Model("hybrid_scheduling")

# Decision variables
pi = model.addVars(S, G, vtype=GRB.BINARY, name="pi")
e = model.addVars(G, C, vtype=GRB.CONTINUOUS, name="e")
delta = model.addVars(G, C, vtype=GRB.CONTINUOUS, name="delta")
s = model.addVar(vtype=GRB.CONTINUOUS, name="s")
s_j_t = model.addVars(G, T, vtype=GRB.CONTINUOUS, name="s_j_t")

# Objective function
model.setObjective(
    gp.quicksum(e[j, k] for j in range(G) for k in C)
    + lambda_param * gp.quicksum(delta[j, k] for j in range(G) for k in C)
    + mu * s,
    GRB.MINIMIZE,
)

# Constraints
# Each student should be assigned to exactly one group
for i in S:
    model.addConstr(gp.quicksum(pi[i, j] for j in range(G)) == 1, name=f"assign_{i}")

# Social distancing constraint and excess
for j in range(G):
    for k in C:
        model.addConstr(
            gp.quicksum(pi[i, j] for i in A[k]) - c[k] <= e[j, k],
            name=f"excess_{j}_{k}",
        )

# Deviation constraint
for j in range(G):
    for k in C:
        model.addConstr(
            -delta[j, k] <= gp.quicksum(pi[i, j] for i in A[k]) - len(A[k]) / G,
            name=f"lower_deviation_{j}_{k}",
        )
        model.addConstr(
            gp.quicksum(pi[i, j] for i in A[k]) - len(A[k]) / G <= delta[j, k],
            name=f"upper_deviation_{j}_{k}",
        )

# Surplus simultaneous excess constraint
for t in range(T):
    for j in range(G):
        model.addConstr(s >= s_j_t[j, t] - E, name=f"surplus_{j}_{t}_s")
        model.addConstr(
            s_j_t[j, t] >= gp.quicksum(e[j, k] for k in C_t[str(t)]),
            name=f"surplus_{j}_{t}",
        )

# Non-negativity constraints
model.addConstrs((delta[j, k] >= 0 for j in range(G) for k in C), name="nonneg_delta")
model.addConstrs((e[j, k] >= 0 for j in range(G) for k in C), name="nonneg_e")
model.addConstr(s >= 0, name="nonneg_s")

# Optimize the model
model.optimize()

# Display results
if model.status == GRB.OPTIMAL:
    print(model.ObjVal)
    from pathlib import Path

    Path("obj.txt").write_text(str(model.ObjVal))
else:
    print("No optimal solution found.")
