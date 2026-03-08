
import os
import numpy as np
import json 
from gurobipy import Model, GRB, quicksum


model = Model("OptimizationProblem")

with open("data.json", "r") as f:
    data = json.load(f)




### Define the parameters

VitaminCPerOrange = data["VitaminCPerOrange"] # shape: [], definition: Units of vitamin C per orange

VitaminAPerOrange = data["VitaminAPerOrange"] # shape: [], definition: Units of vitamin A per orange

SugarPerOrange = data["SugarPerOrange"] # shape: [], definition: Grams of sugar per orange

VitaminCPerGrapefruit = data["VitaminCPerGrapefruit"] # shape: [], definition: Units of vitamin C per grapefruit

VitaminAPerGrapefruit = data["VitaminAPerGrapefruit"] # shape: [], definition: Units of vitamin A per grapefruit

SugarPerGrapefruit = data["SugarPerGrapefruit"] # shape: [], definition: Grams of sugar per grapefruit

MinVitaminC = data["MinVitaminC"] # shape: [], definition: Minimum required units of vitamin C

MinVitaminA = data["MinVitaminA"] # shape: [], definition: Minimum required units of vitamin A

MinOrangeToGrapefruitRatio = data["MinOrangeToGrapefruitRatio"] # shape: [], definition: Minimum ratio of oranges to grapefruits indicating preference



### Define the variables

Oranges = model.addVar(vtype=GRB.INTEGER, name="Oranges")

Grapefruits = model.addVar(vtype=GRB.INTEGER, name="Grapefruits")



### Define the constraints

model.addConstr(VitaminCPerOrange * Oranges + VitaminCPerGrapefruit * Grapefruits >= MinVitaminC)
model.addConstr(VitaminAPerOrange * Oranges + VitaminAPerGrapefruit * Grapefruits >= MinVitaminA)
model.addConstr(Oranges >= MinOrangeToGrapefruitRatio * Grapefruits)
model.addConstr(Oranges >= 0)
model.addConstr(Grapefruits >= 0)


### Define the objective

model.setObjective(SugarPerOrange * Oranges + SugarPerGrapefruit * Grapefruits, GRB.MINIMIZE)


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
