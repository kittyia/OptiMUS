
import os
import numpy as np
import json 
from gurobipy import Model, GRB, quicksum


model = Model("OptimizationProblem")

with open("data.json", "r") as f:
    data = json.load(f)




### Define the parameters

SmallKegCapacity = data["SmallKegCapacity"] # shape: [], definition: Capacity of a small keg in liters

LargeKegCapacity = data["LargeKegCapacity"] # shape: [], definition: Capacity of a large keg in liters

MaxSmallKegsAvailable = data["MaxSmallKegsAvailable"] # shape: [], definition: Maximum number of small kegs available

MaxLargeKegsAvailable = data["MaxLargeKegsAvailable"] # shape: [], definition: Maximum number of large kegs available

SmallKegMultiplier = data["SmallKegMultiplier"] # shape: [], definition: The multiplier for the number of small kegs to be used compared to large kegs

MaxTotalKegs = data["MaxTotalKegs"] # shape: [], definition: Maximum total number of kegs that can be transported

MinLargeKegs = data["MinLargeKegs"] # shape: [], definition: Minimum number of large kegs that must be used



### Define the variables

SmallKegsUsed = model.addVar(vtype=GRB.INTEGER, name="SmallKegsUsed")

LargeKegsUsed = model.addVar(vtype=GRB.INTEGER, name="LargeKegsUsed")



### Define the constraints

model.addConstr(SmallKegsUsed <= MaxSmallKegsAvailable)
model.addConstr(LargeKegsUsed >= MinLargeKegs)
model.addConstr(LargeKegsUsed <= MaxLargeKegsAvailable)
model.addConstr(SmallKegsUsed >= SmallKegMultiplier * LargeKegsUsed)
model.addConstr(SmallKegsUsed + LargeKegsUsed <= MaxTotalKegs)


### Define the objective

model.setObjective(
    SmallKegCapacity * SmallKegsUsed + LargeKegCapacity * LargeKegsUsed,
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
