
import os
import numpy as np
import json 
from gurobipy import Model, GRB, quicksum


model = Model("OptimizationProblem")

with open("data.json", "r") as f:
    data = json.load(f)




### Define the parameters

VitaminCShots = data["VitaminCShots"] # shape: [], definition: Amount of vitamin C required per batch of vitamin shots

VitaminDShots = data["VitaminDShots"] # shape: [], definition: Amount of vitamin D required per batch of vitamin shots

VitaminCPills = data["VitaminCPills"] # shape: [], definition: Amount of vitamin C required per batch of vitamin pills

VitaminDPills = data["VitaminDPills"] # shape: [], definition: Amount of vitamin D required per batch of vitamin pills

MaxBatchesShots = data["MaxBatchesShots"] # shape: [], definition: The maximum number of batches of vitamin shots that can be produced

AvailableVitaminC = data["AvailableVitaminC"] # shape: [], definition: Total available units of vitamin C

AvailableVitaminD = data["AvailableVitaminD"] # shape: [], definition: Total available units of vitamin D

SupplyShots = data["SupplyShots"] # shape: [], definition: Number of people supplied per batch of vitamin shots

SupplyPills = data["SupplyPills"] # shape: [], definition: Number of people supplied per batch of vitamin pills

MinBatchDifference = data["MinBatchDifference"] # shape: [], definition: Minimum number of additional batches of vitamin pills compared to vitamin shots



### Define the variables

batchesShots = model.addVar(vtype=GRB.INTEGER, name="batchesShots")

batchesPills = model.addVar(vtype=GRB.INTEGER, name="batchesPills")



### Define the constraints

model.addConstr(VitaminCShots * batchesShots + VitaminCPills * batchesPills <= AvailableVitaminC)
model.addConstr(VitaminDShots * batchesShots + VitaminDPills * batchesPills <= AvailableVitaminD)
model.addConstr(batchesPills >= batchesShots + MinBatchDifference)
model.addConstr(batchesShots <= MaxBatchesShots)
model.addConstr(batchesShots >= 0)


### Define the objective

model.setObjective(SupplyShots * batchesShots + SupplyPills * batchesPills, GRB.MAXIMIZE)


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
