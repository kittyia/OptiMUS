
import os
import numpy as np
import json 
from gurobipy import Model, GRB, quicksum


model = Model("OptimizationProblem")

with open("data.json", "r") as f:
    data = json.load(f)




### Define the parameters

MasksPerSmallBox = data["MasksPerSmallBox"] # shape: [], definition: Number of masks that fit in a small box

MasksPerLargeBox = data["MasksPerLargeBox"] # shape: [], definition: Number of masks that fit in a large box

MinRatioSmallToLarge = data["MinRatioSmallToLarge"] # shape: [], definition: Minimum ratio of small boxes to large boxes

MinLargeBoxes = data["MinLargeBoxes"] # shape: [], definition: Minimum number of large boxes required

TotalMasksRequired = data["TotalMasksRequired"] # shape: [], definition: Minimum number of masks to distribute



### Define the variables

SmallBoxes = model.addVar(vtype=GRB.INTEGER, name="SmallBoxes")

LargeBoxes = model.addVar(vtype=GRB.INTEGER, name="LargeBoxes")



### Define the constraints

model.addConstr(SmallBoxes >= MinRatioSmallToLarge * LargeBoxes)
model.addConstr(LargeBoxes >= MinLargeBoxes)
model.addConstr(MasksPerSmallBox * SmallBoxes + MasksPerLargeBox * LargeBoxes >= TotalMasksRequired)


### Define the objective

model.setObjective(SmallBoxes + LargeBoxes, GRB.MINIMIZE)


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
