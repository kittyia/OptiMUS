
import os
import numpy as np
import json 
from gurobipy import Model, GRB, quicksum


model = Model("OptimizationProblem")

with open("data.json", "r") as f:
    data = json.load(f)




### Define the parameters

CapacitySmallCrate = data["CapacitySmallCrate"] # shape: [], definition: Number of bananas a small crate can hold

CapacityLargeCrate = data["CapacityLargeCrate"] # shape: [], definition: Number of bananas a large crate can hold

TotalBananas = data["TotalBananas"] # shape: [], definition: Total number of bananas available

MinSmallCrates = data["MinSmallCrates"] # shape: [], definition: Minimum number of small crates to be used

LargeToSmallRatio = data["LargeToSmallRatio"] # shape: [], definition: Minimum multiple of small crates that large crates must be



### Define the variables

SmallCrates = model.addVar(vtype=GRB.INTEGER, name="SmallCrates")

LargeCrates = model.addVar(vtype=GRB.INTEGER, name="LargeCrates")



### Define the constraints

model.addConstr(CapacitySmallCrate * SmallCrates + CapacityLargeCrate * LargeCrates <= TotalBananas)
model.addConstr(LargeCrates >= LargeToSmallRatio * SmallCrates)
model.addConstr(SmallCrates >= MinSmallCrates)
model.addConstr(SmallCrates >= 0)
model.addConstr(LargeCrates >= 0)


### Define the objective

model.setObjective(SmallCrates + LargeCrates, GRB.MAXIMIZE)


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
