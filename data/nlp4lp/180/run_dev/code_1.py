import os
import numpy as np
import json
from gurobipy import Model, GRB, quicksum


model = Model("OptimizationProblem")

with open("data.json", "r") as f:
    data = json.load(f)


### Define the parameters

SmallCrateCapacity = data["SmallCrateCapacity"]
LargeCrateCapacity = data["LargeCrateCapacity"]
MinimumSmallToLargeRatio = data["MinimumSmallToLargeRatio"]
MaxSmallCrates = data["MaxSmallCrates"]
MaxLargeCrates = data["MaxLargeCrates"]
MaxTotalCrates = data["MaxTotalCrates"]
MinLargeCrates = data["MinLargeCrates"]


### Define the variables

SmallCratesUsed = model.addVar(vtype=GRB.INTEGER, name="SmallCratesUsed")
LargeCratesUsed = model.addVar(vtype=GRB.INTEGER, name="LargeCratesUsed")


### Define the constraints

model.addConstr(SmallCratesUsed >= MinimumSmallToLargeRatio * LargeCratesUsed)
model.addConstr(SmallCratesUsed + LargeCratesUsed <= MaxTotalCrates)
model.addConstr(LargeCratesUsed >= MinLargeCrates)
model.addConstr(SmallCratesUsed <= MaxSmallCrates)
model.addConstr(LargeCratesUsed <= MaxLargeCrates)


### Define the objective

model.setObjective(
    SmallCrateCapacity * SmallCratesUsed + LargeCrateCapacity * LargeCratesUsed,
    GRB.MAXIMIZE
)


### Optimize the model

model.optimize()


### Output optimal objective value

if model.status == GRB.OPTIMAL:
    print("Optimal Objective Value: ", model.ObjVal)
    with open("output_solution.txt", "w") as f:
        f.write(str(model.ObjVal))
else:
    with open("output_solution.txt", "w") as f:
        f.write(str(model.status))