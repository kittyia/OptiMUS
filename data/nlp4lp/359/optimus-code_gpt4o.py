import json
from gurobipy import *

# Load data
with open("data.json", "r") as f:
    data = json.load(f)

# Extract data
A_P = data["A_P"]
ell = data["ell"]
F = data["F"]
gamma = data["gamma"]
s = data["s"]
t = data["t"]
V_T = data["V_T"]
L = data["L"]
L_e = data["L_e"]
F_4 = data["F_4"]
B_delta = data["B_delta"]
hat_B_delta = data["hat_B_delta"]
E_delta = data["E_delta"]
hat_E_delta = data["hat_E_delta"]

# Create model
model = Model("WasteCollection")

# Create variables
x = model.addVars(A_P, vtype=GRB.BINARY, name="x")

# Objective: Minimize the length of the route
model.setObjective(quicksum(ell[str(i)][str(j)] * x[i, j] for i, j in A_P), GRB.MINIMIZE)

# Constraints
# Each node in T is visited exactly once
for v in V_T:
    model.addConstr(quicksum(x[i, j] for i, j in A_P if j == v) == 1, name=f"visit_once_{v}")

# Avoid formation of subtours
# Implement subtour elimination constraints using MTZ formulation
u = model.addVars(V_T, vtype=GRB.CONTINUOUS, name="u")
for i, j in A_P:
    if i != s and j != t:
        model.addConstr(u[i] - u[j] + len(V_T) * x[i, j] <= len(V_T) - 1, name=f"subtour_{i}_{j}")

# The trucks directly service all block sides that are too long to be handled under the achique system
for e in L:
    model.addConstr(quicksum(x[i, j] for i, j in L_e[str(e)]) >= 1, name=f"service_{e}")

# Impose that t is the last node visited
model.addConstr(quicksum(x[i, j] for i, j in A_P if j == t) == 1, name="end_at_t")

# Avoid violating traffic restrictions
for (i, j, k) in F:
    model.addConstr(x[i, j] + x[j, k] <= 1, name=f"traffic_restriction_{i}_{j}_{k}")

# Forbidden paths of length three and four
for (u1, u2, u3, u4) in F_4:
    for v in B_delta[str((u1, u2, u3, u4))]:
        model.addConstr(x[v, u2] == 0, name=f"forbidden_B_{v}_{u2}")
    for v in hat_B_delta[str((u1, u2, u3, u4))]:
        model.addConstr(x[v, u3] == 0, name=f"forbidden_hat_B_{v}_{u3}")
    for v in E_delta[str((u1, u2, u3, u4))]:
        model.addConstr(x[u3, v] == 0, name=f"forbidden_E_{u3}_{v}")
    for v in hat_E_delta[str((u1, u2, u3, u4))]:
        model.addConstr(x[u2, v] == 0, name=f"forbidden_hat_E_{u2}_{v}")

# Optimize model
model.optimize()

# Write solution
solution = {"variables": {f"x[{i},{j}]": x[i, j].x for i, j in A_P}, "objective": model.objVal}
with open("solution.json", "w") as f:
    json.dump(solution, f, indent=4)
