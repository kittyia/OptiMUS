
import os
import numpy as np
import json 
from gurobipy import Model, GRB, quicksum


model = Model("OptimizationProblem")

with open("data.json", "r") as f:
    data = json.load(f)




### Define the parameters

NumFarms = data["NumFarms"] # shape: [], definition: Number of farms

NumBerries = data["NumBerries"] # shape: [], definition: Number of berry types

OperatingCost = data["OperatingCost"] # shape: ['NumFarms'], definition: Operating cost per day for each farm

HarvestDelivery = data["HarvestDelivery"] # shape: ['NumFarms', 'NumBerries'], definition: Harvest and delivery rate per day for each farm and berry type

RequiredQuantity = data["RequiredQuantity"] # shape: ['NumBerries'], definition: Required quantity of each berry type to meet contract



### Define the variables

Days = model.addVars(NumFarms, vtype=GRB.CONTINUOUS, name="Days")



### Define the constraints

for b in range(NumBerries):
    model.addConstr(
        sum(HarvestDelivery[f][b] * Days[f] for f in range(NumFarms)) 
        >= RequiredQuantity[b]
    )
for f in range(NumFarms):
    model.addConstr(Days[f] >= 0)


### Define the objective

model.setObjective(quicksum(OperatingCost[i] * Days[i] for i in range(NumFarms)), GRB.MINIMIZE)


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
