import os
import numpy as np
import json
from gurobipy import Model, GRB, quicksum


model = Model("OptimizationProblem")

with open("data.json", "r") as f:
    data = json.load(f)


### Define the parameters

NumMilkTeaTypes = data["NumMilkTeaTypes"]  # Number of different milk tea types
NumResources = data["NumResources"]  # Number of different resources

ResourceUsage = data["ResourceUsage"]  # Resource usage matrix
ProfitPerBottle = data["ProfitPerBottle"]  # Profit per bottle
AvailableResource = data["AvailableResource"]  # Available resources


### Define the variables

NumBottles = model.addVars(NumMilkTeaTypes, vtype=GRB.INTEGER, name="NumBottles")


### Define the constraints

# Milk constraint (resource 0)
model.addConstr(
    quicksum(ResourceUsage[0][j] * NumBottles[j] for j in range(NumMilkTeaTypes))
    <= AvailableResource[0]
)

# Honey constraint (resource 1)
model.addConstr(
    quicksum(ResourceUsage[1][j] * NumBottles[j] for j in range(NumMilkTeaTypes))
    <= AvailableResource[1]
)

# Non-negativity constraints
for j in range(NumMilkTeaTypes):
    model.addConstr(NumBottles[j] >= 0)


### Define the objective

model.setObjective(
    quicksum(ProfitPerBottle[j] * NumBottles[j] for j in range(NumMilkTeaTypes)),
    GRB.MAXIMIZE
)


### Optimize the model

model.optimize()


### Output optimal objective value

if model.status == GRB.OPTIMAL:
    print("Optimal Objective Value: ", model.objVal)
    with open("output_solution.txt", "w") as f:
        f.write(str(model.objVal))
else:
    with open("output_solution.txt", "w") as f:
        f.write(str(model.status))