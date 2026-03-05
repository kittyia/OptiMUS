import json
import gurobipy as gp
from gurobipy import GRB

with open("data.json", "r") as f:
    params = json.load(f)

A_P = params["A_P"]
E_P = params["E_P"]
ell = params["ell"]
# Normalize numeric string keys to integers (JSON keys may be strings)
if ell and isinstance(next(iter(ell.keys())), str):
    ell = {int(i): {int(j): v for j, v in sub.items()} for i, sub in ell.items()}
F = params["F"]
gamma = params["gamma"]
s = params["s"]
t = params["t"]
V_T = params["V_T"]
V_ij = params["V_ij"]
# Sanity check: ensure ell has entries for all ordered pairs in V_T
_missing_ell = [
    (i, j) for i in V_T for j in V_T if i != j and (i not in ell or j not in ell[i])
]
if _missing_ell:
    raise KeyError(
        f"ell missing entries for pairs (sample): {_missing_ell[:10]}{'...' if len(_missing_ell)>10 else ''}"
    )
L = params["L"]
L_e = params["L_e"]
F_4 = params["F_4"]
B_delta = params["B_delta"]
hat_B_delta = params["hat_B_delta"]
E_delta = params["E_delta"]
hat_E_delta = params["hat_E_delta"]

# Create a new model
model = gp.Model("waste_truck_routing")

# Decision variables
x = model.addVars(V_T, V_T, vtype=GRB.BINARY, name="x")
u = model.addVars(V_T, vtype=GRB.CONTINUOUS, name="u")

# Objective function
model.setObjective(
    gp.quicksum(ell[i][j] * x[i, j] for i in V_T for j in V_T if i != j),
    GRB.MINIMIZE,
)

# Constraints
# Each node in T is visited exactly once
for j in V_T:
    model.addConstr(gp.quicksum(x[i, j] for i in V_T if i != j) == 1, name=f"visit_{j}")

for i in V_T:
    model.addConstr(gp.quicksum(x[i, j] for j in V_T if j != i) == 1, name=f"leave_{i}")

# Subtour elimination (standard MTZ formulation)
n = len(V_T)
# Set u_s = 0 and bounds 1..n-1 for other nodes
model.addConstr(u[s] == 0, name=f"u_{s}_zero")
for i in V_T:
    if i != s:
        model.addConstr(u[i] >= 1, name=f"u_lb_{i}")
        model.addConstr(u[i] <= n - 1, name=f"u_ub_{i}")

# MTZ constraints for i != j and i != s and j != s
for i in V_T:
    for j in V_T:
        if i != j and i != s and j != s:
            model.addConstr(u[i] - u[j] + n * x[i, j] <= n - 1, name=f"mtz_{i}_{j}")

# Disallow self-loops explicitly
for i in V_T:
    model.addConstr(x[i, i] == 0, name=f"no_self_{i}")

# Directly service block sides too long for achique system
for e in L:
    # only add constraint if there is at least one T-arc that uses the long arc
    if L_e.get(str(tuple(e))):
        model.addConstr(
            gp.quicksum(x[i, j] for (i, j) in L_e[str(tuple(e))]) >= 1,
            name=f"direct_{e}",
        )
# Ensure t is the last node visited
model.addConstr(x[t, s] == 1, name="last_node")

# Avoid traffic restrictions
for i in V_T:
    for j in V_T:
        if i != j:
            model.addConstr(
                gp.quicksum(x[j, k] for k in V_ij[str((i, j))]) <= 1 - x[i, j],
                name=f"traffic_{i}_{j}",
            )

# Handle forbidden paths with four nodes
for delta in F_4:
    u1, u2, u3, u4 = delta
    model.addConstr(
        gp.quicksum(x[v, u2] for v in B_delta[str(tuple(delta))])
        + x[u2, u3]
        + gp.quicksum(x[u3, v] for v in E_delta[str(tuple(delta))])
        <= 2,
        name=f"forbidden_{delta}",
    )
    model.addConstr(
        gp.quicksum(x[v, u3] for v in hat_B_delta[str(tuple(delta))])
        + gp.quicksum(x[u3, v] for v in E_delta[str(tuple(delta))])
        <= 1,
        name=f"forbidden2_{delta}",
    )
    model.addConstr(
        gp.quicksum(x[v, u2] for v in B_delta[str(tuple(delta))])
        + gp.quicksum(x[u2, v] for v in hat_E_delta[str(tuple(delta))])
        <= 1,
        name=f"forbidden3_{delta}",
    )

# (u bounds and u_s == 0 handled above by explicit constraints)

# Set a modest time limit for larger instances to keep checks quick
model.Params.TimeLimit = 30

# Optimize the model
model.optimize()

# Display results
if model.status == GRB.OPTIMAL:
    print(model.ObjVal)
    from pathlib import Path

    Path("obj.txt").write_text(str(model.ObjVal))
else:
    print("No optimal solution found.")
    # Compute IIS
    model.computeIIS()

    # Write the IIS to a file
    #  model.write("model.ilp")

    # Print the IIS to the console
    print("The following constraints are infeasible:")
    for c in model.getConstrs():
        if c.IISConstr:
            print(f"C: {c.constrName}")

    print("The following variables are infeasible:")
    for v in model.getVars():
        if v.IISLB or v.IISUB:
            print(f"V: {v.varName}")
