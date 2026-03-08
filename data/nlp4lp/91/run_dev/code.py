
import os
import numpy as np
import json 
from gurobipy import Model, GRB, quicksum


model = Model("OptimizationProblem")

with open("data.json", "r") as f:
    data = json.load(f)




### Define the parameters

ProteinAlpha = data["ProteinAlpha"] # shape: [], definition: Amount of protein per bottle of the alpha brand drink

SugarAlpha = data["SugarAlpha"] # shape: [], definition: Amount of sugar per bottle of the alpha brand drink

CaloriesAlpha = data["CaloriesAlpha"] # shape: [], definition: Number of calories per bottle of the alpha brand drink

ProteinOmega = data["ProteinOmega"] # shape: [], definition: Amount of protein per bottle of the omega brand drink

SugarOmega = data["SugarOmega"] # shape: [], definition: Amount of sugar per bottle of the omega brand drink

CaloriesOmega = data["CaloriesOmega"] # shape: [], definition: Number of calories per bottle of the omega brand drink

MinProtein = data["MinProtein"] # shape: [], definition: Minimum total protein required

MinCalories = data["MinCalories"] # shape: [], definition: Minimum total calories required

MaxOmegaFraction = data["MaxOmegaFraction"] # shape: [], definition: Maximum proportion of omega brand drinks allowed



### Define the variables

AlphaBottles = model.addVar(vtype=GRB.INTEGER, name="AlphaBottles")

OmegaBottles = model.addVar(vtype=GRB.INTEGER, name="OmegaBottles")



### Define the constraints

model.addConstr(CaloriesAlpha * AlphaBottles + CaloriesOmega * OmegaBottles >= MinCalories)
model.addConstr(13 * OmegaBottles <= 7 * AlphaBottles)
model.addConstr(AlphaBottles >= 0)
model.addConstr(OmegaBottles >= 0)


### Define the objective

model.setObjective(SugarAlpha * AlphaBottles + SugarOmega * OmegaBottles, GRB.MINIMIZE)


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
