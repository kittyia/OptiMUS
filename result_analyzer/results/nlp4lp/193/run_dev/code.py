
import os
import numpy as np
import json 
from gurobipy import Model, GRB, quicksum


model = Model("OptimizationProblem")

with open("data.json", "r") as f:
    data = json.load(f)




### Define the parameters

NumMilkTeaTypes = data["NumMilkTeaTypes"] # shape: [], definition: Number of different milk tea types to be produced

NumResources = data["NumResources"] # shape: [], definition: Number of different resources used in production

ResourceUsage = data["ResourceUsage"] # shape: ['NumResources', 'NumMilkTeaTypes'], definition: Amount of resource i required to produce one bottle of milk tea type j

ProfitPerBottle = data["ProfitPerBottle"] # shape: ['NumMilkTeaTypes'], definition: Profit earned from selling one bottle of milk tea type j

AvailableResource = data["AvailableResource"] # shape: ['NumResources'], definition: Total available amount of resource i



### Define the variables

NumBottles = model.addVars(NumMilkTeaTypes, vtype=GRB.INTEGER, name="NumBottles")



### Define the constraints

model.addConstr(
    sum(ResourceUsage[0][j] * NumBottles[j] for j in range(NumMilkTeaTypes))
    <= AvailableResource[0]
)
model.addConstr(10 * NumBottles[0] + 5 * NumBottles[1] <= 500)
for j in range(NumMilkTeaTypes):
    model.addConstr(NumBottles[j] >= 0)


### Define the objective

del.setObjective(quicksum(ProfitPerBottle[j] * NumBottles[j] for j in range(NumMilkTeaTypes)), GRB.MAXIMIZE


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
