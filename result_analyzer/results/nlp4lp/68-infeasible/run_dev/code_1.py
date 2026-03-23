import os
import numpy as np
import json
from gurobipy import Model, GRB, quicksum


model = Model("OptimizationProblem")

with open("data.json", "r") as f:
    data = json.load(f)


### Define the parameters

CapacitySmallCrate = data["CapacitySmallCrate"]
CapacityLargeCrate = data["CapacityLargeCrate"]
TotalBananas = data["TotalBananas"]
MinSmallCrates = data["MinSmallCrates"]
LargeToSmallRatio = data["LargeToSmallRatio"]


### Define the variables

SmallCrates = model.addVar(vtype=GRB.INTEGER, name="SmallCrates")
LargeCrates = model.addVar(vtype=GRB.INTEGER, name="LargeCrates")


### Define the constraints

model.addConstr(
    CapacitySmallCrate * SmallCrates +
    CapacityLargeCrate * LargeCrates <= TotalBananas
)

model.addConstr(LargeCrates >= LargeToSmallRatio * SmallCrates)
model.addConstr(SmallCrates >= MinSmallCrates)

# Non-negativity (optional since INTEGER defaults to lb=0, but kept for clarity)
model.addConstr(SmallCrates >= 0)
model.addConstr(LargeCrates >= 0)


### Define the objective

model.setObjective(SmallCrates + LargeCrates, GRB.MAXIMIZE)


### Optimize the model

model.optimize()


### Output results safely

if model.status == GRB.OPTIMAL:
    print("Optimal Objective Value:", model.ObjVal)
    with open("output_solution.txt", "w") as f:
        f.write(str(model.ObjVal))
else:
    print("Optimization was not successful. Status code:", model.status)
    with open("output_solution.txt", "w") as f:
        f.write(str(model.status))