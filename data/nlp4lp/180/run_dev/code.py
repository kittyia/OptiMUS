
import os
import numpy as np
import json 
from gurobipy import Model, GRB, quicksum


model = Model("OptimizationProblem")

with open("data.json", "r") as f:
    data = json.load(f)




### Define the parameters

SmallCrateCapacity = data["SmallCrateCapacity"] # shape: [], definition: Number of grapes a small crate can hold

LargeCrateCapacity = data["LargeCrateCapacity"] # shape: [], definition: Number of grapes a large crate can hold

MinimumSmallToLargeRatio = data["MinimumSmallToLargeRatio"] # shape: [], definition: Minimum ratio of small crates to large crates

MaxSmallCrates = data["MaxSmallCrates"] # shape: [], definition: Maximum number of small crates available

MaxLargeCrates = data["MaxLargeCrates"] # shape: [], definition: Maximum number of large crates available

MaxTotalCrates = data["MaxTotalCrates"] # shape: [], definition: Maximum number of crates the truck can carry

MinLargeCrates = data["MinLargeCrates"] # shape: [], definition: Minimum number of large crates to be used



### Define the variables

SmallCratesUsed = model.addVar(vtype=GRB.INTEGER, name="SmallCratesUsed")

LargeCratesUsed = model.addVar(vtype=GRB.INTEGER, name="LargeCratesUsed")



### Define the constraints

model.addConstr(SmallCratesUsed >= MinimumSmallToLargeRatio * LargeCratesUsed)
model.addConstr(SmallCratesUsed + LargeCratesUsed <= MaxTotalCrates)
model.addConstr(LargeCratesUsed >= MinLargeCrates)
# SmallCratesUsed is defined as an integer variable when created (vtype=GRB.INTEGER),
# so no additional constraint is required to enforce integrality.
# LargeCratesUsed is defined as an integer variable (vtype=GRB.INTEGER),
# so no additional constraint is required to enforce integrality.


### Define the objective

del.setObjective(SmallCrateCapacity * SmallCratesUsed + LargeCrateCapacity * LargeCratesUsed, GRB.MAXIMIZE


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
