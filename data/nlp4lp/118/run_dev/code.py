
import os
import numpy as np
import json 
from gurobipy import Model, GRB, quicksum


model = Model("OptimizationProblem")

with open("data.json", "r") as f:
    data = json.load(f)




### Define the parameters

NumProducts = data["NumProducts"] # shape: [], definition: Number of different products

NumResources = data["NumResources"] # shape: [], definition: Number of different resources

ResourceRequired = data["ResourceRequired"] # shape: ['NumResources', 'NumProducts'], definition: Amount of each resource required to produce one unit of each product

TotalAvailableResources = data["TotalAvailableResources"] # shape: ['NumResources'], definition: Total available units of each resource

MaxLiquidSanitizers = data["MaxLiquidSanitizers"] # shape: [], definition: Maximum number of liquid hand sanitizers that can be produced

CleaningPerUnit = data["CleaningPerUnit"] # shape: ['NumProducts'], definition: Number of hands cleaned by each unit of each product



### Define the variables

LiquidSanitizers = model.addVar(vtype=GRB.INTEGER, name="LiquidSanitizers")

FoamSanitizers = model.addVar(vtype=GRB.INTEGER, name="FoamSanitizers")



### Define the constraints

model.addConstr(40 * LiquidSanitizers + 60 * FoamSanitizers <= 2000)
model.addConstr(50 * LiquidSanitizers + 40 * FoamSanitizers <= 2100)
model.addConstr(FoamSanitizers >= LiquidSanitizers)
model.addConstr(LiquidSanitizers >= 0)


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
