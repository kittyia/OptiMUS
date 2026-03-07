
import os
import numpy as np
import json 
from gurobipy import Model, GRB, quicksum


model = Model("OptimizationProblem")

with open("data.json", "r") as f:
    data = json.load(f)




### Define the parameters

M = data["M"] # shape: [], definition: Number of different products produced by the firm

N = data["N"] # shape: [], definition: Number of different raw materials used by the firm

Available = data["Available"] # shape: ['N'], definition: Available amount of raw material i

Requirements = data["Requirements"] # shape: ['N', 'M'], definition: Amount of raw material i required to produce one unit of product j

Prices = data["Prices"] # shape: ['M'], definition: Revenue earned from selling one unit of product j



### Define the variables

Production = model.addVars(M, vtype=GRB.CONTINUOUS, name="Production")



### Define the constraints

for i in range(N):
    model.addConstr(
        sum(Requirements[i][j] * Production[j] for j in range(M)) <= Available[i]
    )
for j in range(M):
    model.addConstr(Production[j] >= 0)


### Define the objective

model.setObjective(quicksum(Prices[j] * Production[j] for j in range(M)), GRB.MAXIMIZE)


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
