
import os
import numpy as np
import json 
from gurobipy import Model, GRB, quicksum


model = Model("OptimizationProblem")

with open("data.json", "r") as f:
    data = json.load(f)




### Define the parameters

SmallBottleCapacity = data["SmallBottleCapacity"] # shape: [], definition: Capacity of a small bottle in units of honey

LargeBottleCapacity = data["LargeBottleCapacity"] # shape: [], definition: Capacity of a large bottle in units of honey

MaxSmallBottles = data["MaxSmallBottles"] # shape: [], definition: Maximum number of small bottles available

MaxLargeBottles = data["MaxLargeBottles"] # shape: [], definition: Maximum number of large bottles available

MinRatioSmallToLarge = data["MinRatioSmallToLarge"] # shape: [], definition: Minimum ratio of small bottles to large bottles

MaxTotalBottles = data["MaxTotalBottles"] # shape: [], definition: Maximum total number of bottles that can be transported

MinLargeBottles = data["MinLargeBottles"] # shape: [], definition: Minimum number of large bottles that must be used



### Define the variables

SmallBottlesUsed = model.addVar(vtype=GRB.INTEGER, name="SmallBottlesUsed")

LargeBottlesUsed = model.addVar(vtype=GRB.INTEGER, name="LargeBottlesUsed")



### Define the constraints

model.addConstr(SmallBottlesUsed >= MinRatioSmallToLarge * LargeBottlesUsed)
model.addConstr(SmallBottlesUsed + LargeBottlesUsed <= MaxTotalBottles)
model.addConstr(LargeBottlesUsed >= MinLargeBottles)
# Integrality is enforced by defining SmallBottlesUsed and LargeBottlesUsed 
# with vtype=GRB.INTEGER when creating the variables.


### Define the objective

model.setObjective(
    SmallBottleCapacity * SmallBottlesUsed + 
    LargeBottleCapacity * LargeBottlesUsed,
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
