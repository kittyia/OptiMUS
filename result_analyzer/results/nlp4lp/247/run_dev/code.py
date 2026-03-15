
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

CatalystUnits = model.addVars(NumCatalysts, vtype=GRB.CONTINUOUS, name="CatalystUnits")



### Define the constraints

model.addConstr(
    sum(ResourceRequirement[0][c] * CatalystUnits[c] for c in range(NumCatalysts))
    <= TotalResource[0]
)
model.addConstr(
    sum(ResourceRequirement[1][c] * CatalystUnits[c] for c in range(NumCatalysts))
    <= TotalResource[1]
)
for c in range(NumCatalysts):
    model.addConstr(CatalystUnits[c] >= 0)


### Define the objective

model.setObjective(quicksum(ConversionRate[c] * CatalystUnits[c] for c in range(NumCatalysts)), GRB.MAXIMIZE)


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
