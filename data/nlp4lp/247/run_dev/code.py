
import os
import numpy as np
import json 
from gurobipy import Model, GRB, quicksum


model = Model("OptimizationProblem")

with open("data.json", "r") as f:
    data = json.load(f)




### Define the parameters

NumCatalysts = data["NumCatalysts"] # shape: [], definition: Number of catalyst types

NumResources = data["NumResources"] # shape: [], definition: Number of resources

ResourceRequirement = data["ResourceRequirement"] # shape: ['NumResources', 'NumCatalysts'], definition: Amount of resource r required per unit of catalyst c

ConversionRate = data["ConversionRate"] # shape: ['NumCatalysts'], definition: Conversion rate per unit of catalyst c

TotalResource = data["TotalResource"] # shape: ['NumResources'], definition: Total amount of resource r available



### Define the variables

PalladiumHeavy = model.addVar(vtype=GRB.CONTINUOUS, name="PalladiumHeavy")

PlatinumHeavy = model.addVar(vtype=GRB.CONTINUOUS, name="PlatinumHeavy")



### Define the constraints

model.addConstr(15 * PalladiumHeavy + 20 * PlatinumHeavy <= 450)
model.addConstr(25 * PalladiumHeavy + 14 * PlatinumHeavy <= 390)
model.addConstr(PalladiumHeavy >= 0)
model.addConstr(PlatinumHeavy >= 0)


### Define the objective

model.setObjective(5 * PalladiumHeavy + 4 * PlatinumHeavy, GRB.MAXIMIZE)


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
