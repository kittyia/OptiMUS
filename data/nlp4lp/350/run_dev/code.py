
import os
import numpy as np
import json 
from gurobipy import Model, GRB, quicksum


model = Model("OptimizationProblem")

with open("data.json", "r") as f:
    data = json.load(f)




### Define the parameters

N = data["N"] # shape: [], definition: Number of translators

Cost = data["Cost"] # shape: ['N'], definition: Cost of translator i

Languages = data["Languages"] # shape: ['N'], definition: Set of languages that translator i can translate

M = data["M"] # shape: [], definition: Number of required languages

RequiredLanguages = data["RequiredLanguages"] # shape: ['M'], definition: List of required languages



### Define the variables

x = model.addVars(N, vtype=GRB.BINARY, name="x")



### Define the constraints

for m in RequiredLanguages:
    model.addConstr(sum(x[i] for i in range(N) if m in Languages[i]) >= 1)
for i in range(N):
    model.addConstr(x[i] >= 0)
    model.addConstr(x[i] <= 1)


### Define the objective

model.setObjective(quicksum(Cost[i] * x[i] for i in range(N)), GRB.MINIMIZE)


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
