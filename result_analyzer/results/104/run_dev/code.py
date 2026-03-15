
import os
import numpy as np
import json 
from gurobipy import Model, GRB, quicksum


model = Model("OptimizationProblem")

with open("data.json", "r") as f:
    data = json.load(f)




### Define the parameters

FatApple = data["FatApple"] # shape: [], definition: Fat units per serving of apple flavored baby food

FolateApple = data["FolateApple"] # shape: [], definition: Folate units per serving of apple flavored baby food

FatCarrot = data["FatCarrot"] # shape: [], definition: Fat units per serving of carrot flavored baby food

FolateCarrot = data["FolateCarrot"] # shape: [], definition: Folate units per serving of carrot flavored baby food

AppleToCarrotRatio = data["AppleToCarrotRatio"] # shape: [], definition: Multiplier for the number of apple servings relative to carrot servings

MinCarrotServings = data["MinCarrotServings"] # shape: [], definition: Minimum servings of carrot flavored baby food

MaxFolate = data["MaxFolate"] # shape: [], definition: Maximum total folate units allowed



### Define the variables

AppleServings = model.addVar(vtype=GRB.INTEGER, name="AppleServings")

CarrotServings = model.addVar(vtype=GRB.INTEGER, name="CarrotServings")



### Define the constraints

model.addConstr(AppleServings == AppleToCarrotRatio * CarrotServings)
model.addConstr(CarrotServings >= MinCarrotServings)
model.addConstr(FolateApple * AppleServings + FolateCarrot * CarrotServings <= MaxFolate)


### Define the objective

model.setObjective(FatApple * AppleServings + FatCarrot * CarrotServings, GRB.MAXIMIZE)


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
