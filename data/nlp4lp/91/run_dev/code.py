
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

Alpha = model.addVar(vtype=GRB.INTEGER, name="Alpha")

Omega = model.addVar(vtype=GRB.INTEGER, name="Omega")



### Define the constraints

model.addConstr(CaloriesAlpha * Alpha + CaloriesOmega * Omega >= MinCalories)
model.addConstr(Omega <= MaxOmegaFraction * (Alpha + Omega))
model.addConstr(Alpha >= 0)
model.addConstr(Omega >= 0)


### Define the objective

model.setObjective(SugarAlpha * Alpha + SugarOmega * Omega, GRB.MINIMIZE)


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
