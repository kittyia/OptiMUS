
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

smallBoxes = model.addVar(vtype=GRB.INTEGER, name="smallBoxes")

largeBoxes = model.addVar(vtype=GRB.INTEGER, name="largeBoxes")



### Define the constraints

model.addConstr(smallBoxes >= MinRatioSmallToLarge * largeBoxes)
model.addConstr(largeBoxes >= MinLargeBoxes)
model.addConstr(MasksPerSmallBox * smallBoxes + MasksPerLargeBox * largeBoxes >= TotalMasksRequired)
model.addConstr(smallBoxes >= 0)
model.addConstr(largeBoxes >= 0)


### Define the objective




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
