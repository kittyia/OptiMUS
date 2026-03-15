
import os
import numpy as np
import json 
from gurobipy import Model, GRB, quicksum


model = Model("OptimizationProblem")

with open("data.json", "r") as f:
    data = json.load(f)




### Define the parameters

TotalLand = data["TotalLand"] # shape: [], definition: Total land available for operations

NumWellTypes = data["NumWellTypes"] # shape: [], definition: Number of different well types

ProductionPerAcre = data["ProductionPerAcre"] # shape: ['NumWellTypes'], definition: Oil production per acre for each well type

PollutionPerAcre = data["PollutionPerAcre"] # shape: ['NumWellTypes'], definition: Pollution generated per acre for each well type

DrillBitsPerAcre = data["DrillBitsPerAcre"] # shape: ['NumWellTypes'], definition: Drill bits required per acre for each well type

TotalDrillBits = data["TotalDrillBits"] # shape: [], definition: Total available drill bits

MaxPollution = data["MaxPollution"] # shape: [], definition: Maximum allowed pollution units



### Define the variables

Acres = model.addVars(NumWellTypes, vtype=GRB.CONTINUOUS, name="Acres")



### Define the constraints

model.addConstr(
    sum(Acres[w] for w in range(NumWellTypes)) <= TotalLand
)
model.addConstr(
    sum(PollutionPerAcre[i] * Acres[i] for i in range(NumWellTypes)) <= MaxPollution
)
for i in range(NumWellTypes):
    model.addConstr(Acres[i] >= 0)


### Define the objective

model.setObjective(quicksum(ProductionPerAcre[i] * Acres[i] for i in range(NumWellTypes)), GRB.MAXIMIZE)


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
