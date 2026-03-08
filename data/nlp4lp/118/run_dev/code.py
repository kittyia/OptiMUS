
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

Liquid = model.addVar(vtype=GRB.INTEGER, name="Liquid")

Foam = model.addVar(vtype=GRB.INTEGER, name="Foam")



### Define the constraints

model.addConstr(40 * Liquid + 60 * Foam <= 2000)
model.addConstr(50 * Liquid + 40 * Foam <= 2100)
model.addConstr(Foam >= Liquid)
model.addConstr(Liquid <= MaxLiquidSanitizers)
model.addConstr(Liquid >= 0)
model.addConstr(Foam >= 0)


### Define the objective

model.setObjective(30 * Liquid + 20 * Foam, GRB.MAXIMIZE)


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
