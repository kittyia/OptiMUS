import os
import numpy as np
import json
from gurobipy import Model, GRB, quicksum


model = Model("OptimizationProblem")

with open("data.json", "r") as f:
    data = json.load(f)

### Define the parameters

Y = data["y"]  # Observed values of the dependent variable
X = data["x"]  # Observed values of the independent variable
K = len(Y)     # Number of data points

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