import json
from gurobipy import *

# 1. Load data
with open("data.json", "r") as f:
    data = json.load(f)

J = data["J"]          # number of decision-making units
M = data["M"]          # number of inputs
N = data["N"]          # number of outputs
x = data["x_m_j"]      # inputs  (shape M x J)
y = data["y_n_j"]      # outputs (shape N x J)

# 2. Build model
model = Model("DEA")

# Decision variables
w = [model.addVar(lb=-GRB.INFINITY, name=f"w_{m}") for m in range(M)]
u = [model.addVar(lb=-GRB.INFINITY, name=f"u_{n}") for n in range(N)]
v = model.addVar(lb=-GRB.INFINITY, name="v")

model.update()

# Constraint 1:  sum_{n,j} u_n * y_nj == 1
expr_scale = quicksum(u[n] * y[n][j] for n in range(N) for j in range(J))
model.addConstr(expr_scale == 1, name="scale")

# Constraint 2:  sum_m w_m * x_mj - sum_n u_n * y_nj - v >= 0  for all j
for j in range(J):
    expr = quicksum(w[m] * x[m][j] for m in range(M)) \
           - quicksum(u[n] * y[n][j] for n in range(N)) - v
    model.addConstr(expr >= 0, name=f"DMU_{j}")

# Objective:  minimize sum_{m,j} w_m * x_mj - v
objective = quicksum(w[m] * x[m][j] for m in range(M) for j in range(J)) - v
model.setObjective(objective, GRB.MINIMIZE)

# 3. Optimize
model.optimize()

# 4. Write solution
solution = {
    "variables": {f"w_{m}": w[m].X for m in range(M)} |
                 {f"u_{n}": u[n].X for n in range(N)} |
                 {"v": v.X},
    "objective": model.objVal
}

with open("solution.json", "w") as f:
    json.dump(solution, f, indent=4)
