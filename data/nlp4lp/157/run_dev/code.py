
import os
import numpy as np
import json 
from gurobipy import Model, GRB, quicksum


model = Model("OptimizationProblem")

with open("data.json", "r") as f:
    data = json.load(f)




### Define the parameters

SmallWagonCapacity = data["SmallWagonCapacity"] # shape: [], definition: Capacity of a small wagon in units of ore

LargeWagonCapacity = data["LargeWagonCapacity"] # shape: [], definition: Capacity of a large wagon in units of ore

MinSmallToLargeRatio = data["MinSmallToLargeRatio"] # shape: [], definition: Minimum ratio of small wagons to large wagons

MinLargeWagons = data["MinLargeWagons"] # shape: [], definition: Minimum number of large wagons required

TotalOre = data["TotalOre"] # shape: [], definition: Total units of ore to be transported



### Define the variables

SmallWagons = model.addVar(vtype=GRB.INTEGER, name="SmallWagons")

LargeWagons = model.addVar(vtype=GRB.INTEGER, name="LargeWagons")



### Define the constraints

model.addConstr(SmallWagonCapacity * SmallWagons + LargeWagonCapacity * LargeWagons >= TotalOre)
model.addConstr(SmallWagons >= MinSmallToLargeRatio * LargeWagons)
model.addConstr(LargeWagons >= MinLargeWagons)
model.addConstr(SmallWagons >= 0)
model.addConstr(LargeWagons >= 0)


### Define the objective

model.setObjective(SmallWagons + LargeWagons, GRB.MINIMIZE)


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
