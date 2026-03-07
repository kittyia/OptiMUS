
import os
import numpy as np
import json 
from gurobipy import Model, GRB, quicksum


model = Model("OptimizationProblem")

with open("data.json", "r") as f:
    data = json.load(f)




### Define the parameters

OtterTricks = data["OtterTricks"] # shape: [], definition: Number of tricks an otter can perform at a time

OtterTreats = data["OtterTreats"] # shape: [], definition: Number of treats an otter requires to perform at a time

DolphinTricks = data["DolphinTricks"] # shape: [], definition: Number of tricks a dolphin can perform at a time

DolphinTreats = data["DolphinTreats"] # shape: [], definition: Number of treats a dolphin requires to perform at a time

MinDolphins = data["MinDolphins"] # shape: [], definition: Minimum number of dolphins required

MaxOtterPercentage = data["MaxOtterPercentage"] # shape: [], definition: Maximum percentage of performers that can be otters

TotalTreats = data["TotalTreats"] # shape: [], definition: Total number of treats available



### Define the variables

Otters = model.addVar(vtype=GRB.INTEGER, name="Otters")

Dolphins = model.addVar(vtype=GRB.INTEGER, name="Dolphins")



### Define the constraints

model.addConstr(OtterTreats * Otters + DolphinTreats * Dolphins <= TotalTreats)
model.addConstr(Dolphins >= MinDolphins)
model.addConstr(Otters <= MaxOtterPercentage * (Otters + Dolphins))
model.addConstr(Otters >= 0)


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
