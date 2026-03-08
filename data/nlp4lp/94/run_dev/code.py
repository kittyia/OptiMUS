
import os
import numpy as np
import json 
from gurobipy import Model, GRB, quicksum


model = Model("OptimizationProblem")

with open("data.json", "r") as f:
    data = json.load(f)




### Define the parameters

VitaminDOrange = data["VitaminDOrange"] # shape: [], definition: Amount of vitamin D in each box of orange juice

VitaminCOrange = data["VitaminCOrange"] # shape: [], definition: Amount of vitamin C in each box of orange juice

VitaminDApple = data["VitaminDApple"] # shape: [], definition: Amount of vitamin D in each box of apple juice

VitaminCApple = data["VitaminCApple"] # shape: [], definition: Amount of vitamin C in each box of apple juice

PreferenceRatio = data["PreferenceRatio"] # shape: [], definition: Minimum ratio of apple juice boxes to orange juice boxes

MinimumOrangeBoxes = data["MinimumOrangeBoxes"] # shape: [], definition: Minimum number of orange juice boxes to be consumed

MaxVitaminC = data["MaxVitaminC"] # shape: [], definition: Maximum allowed units of vitamin C intake



### Define the variables

AppleBoxes = model.addVar(vtype=GRB.INTEGER, name="AppleBoxes")

OrangeBoxes = model.addVar(vtype=GRB.INTEGER, name="OrangeBoxes")



### Define the constraints

model.addConstr(AppleBoxes >= PreferenceRatio * OrangeBoxes)
model.addConstr(OrangeBoxes >= MinimumOrangeBoxes)
model.addConstr(VitaminCOrange * OrangeBoxes + VitaminCApple * AppleBoxes <= MaxVitaminC)


### Define the objective

model.setObjective(VitaminDOrange * OrangeBoxes + VitaminDApple * AppleBoxes, GRB.MAXIMIZE)


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
