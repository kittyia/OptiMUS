import os
import numpy as np
import json
from gurobipy import Model, GRB, quicksum

model = Model("OptimizationProblem")

with open("data.json", "r") as f:
    data = json.load(f)

### Define the parameters (robust to key capitalization)

Y = data.get("y") if "y" in data else data.get("Y")
X = data.get("x") if "x" in data else data.get("X")

if Y is None or X is None:
    raise KeyError("Input JSON must contain keys 'y' and 'x' (case-insensitive).")

K = len(Y)

### Define the variables

# Regression coefficients (unrestricted in sign)
slope = model.addVar(vtype=GRB.CONTINUOUS, lb=-GRB.INFINITY, name="slope")
intercept = model.addVar(vtype=GRB.CONTINUOUS, lb=-GRB.INFINITY, name="intercept")

# Absolute deviation variables
d = model.addVars(K, vtype=GRB.CONTINUOUS, lb=0.0, name="d")

### Define the constraints

for k in range(K):
    model.addConstr(Y[k] - (slope * X[k] + intercept) <= d[k])
    model.addConstr(slope * X[k] + intercept - Y[k] <= d[k])

### Define the objective

model.setObjective(quicksum(d[k] for k in range(K)), GRB.MINIMIZE)

### Optimize the model

model.optimize()

### Output results

if model.status == GRB.OPTIMAL:
    solution = {
        "intercept": intercept.X,
        "slope": slope.X
    }
    with open("output_solution.txt", "w") as f:
        json.dump(solution, f)
else:
    with open("output_solution.txt", "w") as f:
        f.write(str(model.status))