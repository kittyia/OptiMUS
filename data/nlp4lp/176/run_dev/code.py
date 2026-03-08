
import os
import numpy as np
import json 
from gurobipy import Model, GRB, quicksum


model = Model("OptimizationProblem")

with open("data.json", "r") as f:
    data = json.load(f)




### Define the parameters

BrickCapacityCow = data["BrickCapacityCow"] # shape: [], definition: Number of bricks a cow can carry on its back

BrickCapacityElephant = data["BrickCapacityElephant"] # shape: [], definition: Number of bricks an elephant can carry on its back

MaxElephantsToCowsRatio = data["MaxElephantsToCowsRatio"] # shape: [], definition: Maximum ratio of elephants to cows

MaxCowsToElephantsRatio = data["MaxCowsToElephantsRatio"] # shape: [], definition: Maximum ratio of cows to elephants

RequiredBricks = data["RequiredBricks"] # shape: [], definition: Minimum number of bricks to transport



### Define the variables

cows = model.addVar(vtype=GRB.INTEGER, name="cows")

elephants = model.addVar(vtype=GRB.INTEGER, name="elephants")



### Define the constraints

model.addConstr(BrickCapacityCow * cows + BrickCapacityElephant * elephants >= RequiredBricks)
model.addConstr(elephants <= cows)
model.addConstr(cows <= 2 * elephants)
model.addConstr(cows >= 0)
model.addConstr(elephants >= 0)


### Define the objective

model.setObjective(cows + elephants, GRB.MINIMIZE)


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
