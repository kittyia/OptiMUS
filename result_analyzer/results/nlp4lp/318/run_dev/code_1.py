ython
import os
import numpy as np
import json
from gurobipy import Model, GRB, quicksum

model = Model("OptimizationProblem")

with open("data.json", "r") as f:
    data = json.load(f)

### Define the parameters (infer sizes from data to avoid index mismatch)

Benefit = data["benefit"]            # shape: K x L
Communication = data["communication"]  # shape: K x K
Cost = data["cost"]                  # shape: L x L

K = len(Benefit)                     # Number of departments
L = len(Benefit[0])                  # Number of locations

### Define the variables

islocated = model.addVars(K, L, vtype=GRB.BINARY, name="islocated")

### Define the constraints

# Each department must be located in exactly one city
for k in range(K):
    model.addConstr(quicksum(islocated[k, l] for l in range(L)) == 1)

# No more than 3 departments per city
for l in range(L):
    model.addConstr(quicksum(islocated[k, l] for k in range(K)) <= 3)

### Define the objective (quadratic)

model.setObjective(
    quicksum(
        Communication[k][j] * Cost[l][m] * islocated[k, l] * islocated[j, m]
        for k in range(K)
        for j in range(K)
        for l in range(L)
        for m in range(L)
    )
    - quicksum(
        Benefit[k][l] * islocated[k, l]
        for k in range(K)
        for l in range(L)
    ),
    GRB.MINIMIZE
)

### Optimize the model

model.optimize()

### Output optimal objective value

if model.status == GRB.OPTIMAL:
    print("Optimal Objective Value: ", model.objVal)
    with open("output_solution.txt", "w") as f:
        f.write(str(model.objVal))
else:
    with open("output_solution.txt", "w") as f:
        f.write(str(model.status))
``