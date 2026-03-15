import os
import numpy as np
import json 
from gurobipy import Model, GRB, quicksum


model = Model("OptimizationProblem")

with open("data.json", "r") as f:
    data = json.load(f)


### Define the parameters

SmallKegCapacity = data["SmallKegCapacity"]  # Capacity of a small keg in liters
LargeKegCapacity = data["LargeKegCapacity"]  # Capacity of a large keg in liters
MaxSmallKegsAvailable = data["MaxSmallKegsAvailable"]  # Maximum number of small kegs available
MaxLargeKegsAvailable = data["MaxLargeKegsAvailable"]  # Maximum number of large kegs available
SmallKegMultiplier = data["SmallKegMultiplier"]  # Multiplier for small kegs compared to large kegs
MaxTotalKegs = data["MaxTotalKegs"]  # Maximum total number of kegs that can be transported
MinLargeKegs = data["MinLargeKegs"]  # Minimum number of large kegs that must be used


### Define the variables

smallKegsUsed = model.addVar(vtype=GRB.INTEGER, name="smallKegsUsed")
largeKegsUsed = model.addVar(vtype=GRB.INTEGER, name="largeKegsUsed")


### Define the constraints

model.addConstr(smallKegsUsed <= MaxSmallKegsAvailable)
model.addConstr(largeKegsUsed <= MaxLargeKegsAvailable)
model.addConstr(smallKegsUsed >= SmallKegMultiplier * largeKegsUsed)
model.addConstr(smallKegsUsed + largeKegsUsed <= MaxTotalKegs)
model.addConstr(largeKegsUsed >= MinLargeKegs)


### Define the objective

model.setObjective(
    SmallKegCapacity * smallKegsUsed + LargeKegCapacity * largeKegsUsed,
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
``