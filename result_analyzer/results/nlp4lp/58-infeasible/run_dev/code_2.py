import os
import numpy as np
import json
from gurobipy import Model, GRB, quicksum


model = Model("OptimizationProblem")

with open("data.json", "r") as f:
    data = json.load(f)


# Define the parameters
KidsBottleCapacity = data["KidsBottleCapacity"]
AdultBottleCapacity = data["AdultBottleCapacity"]
AdultToKidsRatio = data["AdultToKidsRatio"]
MinKidsBottles = data["MinKidsBottles"]
AvailableSyrup = data["AvailableSyrup"]


# Define the variables
KidsBottles = model.addVar(vtype=GRB.INTEGER, name="KidsBottles")
AdultBottles = model.addVar(vtype=GRB.INTEGER, name="AdultBottles")


# Define the constraints
model.addConstr(KidsBottleCapacity * KidsBottles + AdultBottleCapacity * AdultBottles <= AvailableSyrup)
model.addConstr(AdultBottles >= AdultToKidsRatio * KidsBottles)
model.addConstr(KidsBottles >= MinKidsBottles)
model.addConstr(KidsBottles >= 0)
model.addConstr(AdultBottles >= 0)


# Define the objective
model.setObjective(KidsBottles + AdultBottles, GRB.MAXIMIZE)


# Optimize the model
model.optimize()


# Output optimal objective value
if model.status == GRB.OPTIMAL:
    print("Optimal Objective Value: ", model.ObjVal)
    with open("output_solution.txt", "w") as f:
        f.write(str(model.ObjVal))
else:
    with open("output_solution.txt", "w") as f:
        f.write(str(model.status))