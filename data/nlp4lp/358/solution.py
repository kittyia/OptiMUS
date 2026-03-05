import json
from gurobipy import Model, GRB


with open('data.json', 'r') as f:
    inputs = json.load(f)

J = inputs['J']
M = inputs['M']
N = inputs['N']
x_m_j = inputs['x_m_j']
y_n_j = inputs['y_n_j']

model = Model("TransitMonitoringOptimization")

w = model.addVars(M, vtype=GRB.CONTINUOUS, name="w")
u = model.addVars(N, vtype=GRB.CONTINUOUS, name="u")
v = model.addVar(vtype=GRB.CONTINUOUS, name="v")

model.setObjective(sum(w[m] * x_m_j[m][0] for m in range(M)) - v, GRB.MINIMIZE)

model.addConstr(sum(u[n] * y_n_j[n][0] for n in range(N)) == 1, name="OutputWeightSum")

for j in range(J):
    model.addConstr(
        sum(w[m] * x_m_j[m][j] for m in range(M)) - sum(u[n] * y_n_j[n][j] for n in range(N)) - v >= 0,
        name=f"EfficiencyConstraint_{j}"
    )

for m in range(M):
    model.addConstr(w[m] >= 0, name=f"NonNegative_w_{m}")

for n in range(N):
    model.addConstr(u[n] >= 0, name=f"NonNegative_u_{n}")

model.optimize()

# Extract results
if model.status == GRB.OPTIMAL:
    print(f"Obj: {model.objVal}")
    from pathlib import Path
    Path("obj.txt").write_text(str(model.objVal))

    solution_w = model.getAttr('x', w)
    solution_u = model.getAttr('x', u)
    print("w:", solution_w)
    print("u:", solution_u)
    print("v:", v.X)

else:
    print("No optimal solution found.")
