
import os
import numpy as np
import json 
from gurobipy import Model, GRB, quicksum


model = Model("OptimizationProblem")

with open("data.json", "r") as f:
    data = json.load(f)




### Define the parameters

K = data["K"] # shape: [], definition: Number of departments

L = data["L"] # shape: [], definition: Number of possible locations

Benefit = data["Benefit"] # shape: ['K', 'L'], definition: Benefit of department k being located at location l

Communication = data["Communication"] # shape: ['K', 'K'], definition: Communication costs between departments k and j

Cost = data["Cost"] # shape: ['L', 'L'], definition: Cost of locating at location l with requirement m



### Define the variables

islocated = model.addVars(K, L, vtype=GRB.BINARY, name="islocated")



### Define the constraints

for k in range(K):
    model.addConstr(sum(islocated[k, l] for l in range(L)) == 1)
for l in range(L):
    model.addConstr(
        sum(islocated[k, l] for k in range(K)) <= 3
    )
for k in range(K):
    for l in range(L):
        model.addConstr(islocated[k, l] >= 0)
        model.addConstr(islocated[k, l] <= 1)


### Define the objective

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

print("Optimal Objective Value: ", model.objVal)


if model.status == GRB.OPTIMAL:
    with open("output_solution.txt", "w") as f:
        f.write(str(model.objVal))
    print("Optimal Objective Value: ", model.objVal)
else:
    with open("output_solution.txt", "w") as f:
        f.write(model.status)
