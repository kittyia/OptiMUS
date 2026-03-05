import json
from gurobipy import *

# Load data
with open("data.json", "r") as f:
    data = json.load(f)

# Extract data
J = data["J"]
M = data["M"]
N = data["N"]
x_m_j = data["x_m_j"]
y_n_j = data["y_n_j"]

# Create a new model
model = Model()

# Add variables
w = model.addVars(M, lb=0, name="w")
u = model.addVars(N, lb=0, name="u")
v = model.addVar(lb=-GRB.INFINITY, name="v")

# Set objective: Minimize the scaled sum of weighted inputs minus a scale factor v
model.setObjective(quicksum(w[m] * x_m_j[m][0] for m in range(M)) - v, GRB.MINIMIZE)

# Add constraints
# Constraint 1: The sum of the weights given to the output times the amount of output from all y_n_j should be 1
model.addConstr(quicksum(u[n] * y_n_j[n][0] for n in range(N)) == 1, "c1")

# Constraint 2: The difference of the sum of the weights given to the inputs times the inputs minus the sum of the weight given to the outputs times the outputs minus the scale factor v should be more than or equal for 0 for all j
for j in range(J):
    model.addConstr(
        quicksum(w[m] * x_m_j[m][j] for m in range(M)) - 
        quicksum(u[n] * y_n_j[n][j] for n in range(N)) - v >= 0, 
        f"c2_{j}"
    )

# Optimize the model
model.optimize()

# Write the solution to a JSON file
solution = {
    "variables": {f"w_{m}": w[m].X for m in range(M)} | {f"u_{n}": u[n].X for n in range(N)} | {"v": v.X},
    "objective": model.objVal
}

with open("solution.json", "w") as f:
    json.dump(solution, f, indent=4)
