
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

NumberOfOtters = model.addVar(vtype=GRB.INTEGER, name="NumberOfOtters")

NumberOfDolphins = model.addVar(vtype=GRB.INTEGER, name="NumberOfDolphins")



### Define the constraints

model.addConstr(OtterTreats * NumberOfOtters + DolphinTreats * NumberOfDolphins <= TotalTreats)
model.addConstr(NumberOfDolphins >= MinDolphins)
model.addConstr(7 * NumberOfOtters <= 3 * NumberOfDolphins)
model.addConstr(NumberOfOtters >= 0)
model.addConstr(NumberOfOtters >= 0)
model.addConstr(NumberOfDolphins >= 0)


### Define the objective

model.setObjective(
    OtterTricks * NumberOfOtters + DolphinTricks * NumberOfDolphins,
    GRB.MAXIMIZE
)


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
