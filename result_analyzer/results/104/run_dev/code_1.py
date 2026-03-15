import os
import numpy as np
import json
from gurobipy import Model, GRB, quicksum


model = Model("OptimizationProblem")

with open("data.json", "r") as f:
    data = json.load(f)


### Define the parameters

FatApple = data["FatApple"]  # Fat units per serving of apple flavored baby food
FolateApple = data["FolateApple"]  # Folate units per serving of apple flavored baby food
FatCarrot = data["FatCarrot"]  # Fat units per serving of carrot flavored baby food
FolateCarrot = data["FolateCarrot"]  # Folate units per serving of carrot flavored baby food
AppleToCarrotRatio = data["AppleToCarrotRatio"]  # Multiplier for apple servings relative to carrot servings
MinCarrotServings = data["MinCarrotServings"]  # Minimum carrot servings
MaxFolate = data["MaxFolate"]  # Maximum total folate units allowed


### Define the variables

AppleServings = model.addVar(vtype=GRB.CONTINUOUS, name="AppleServings")
CarrotServings = model.addVar(vtype=GRB.CONTINUOUS, name="CarrotServings")


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
        f.write(str(model.status))