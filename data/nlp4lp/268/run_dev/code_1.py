import os
import numpy as np
import json
from gurobipy import Model, GRB, quicksum

model = Model("OptimizationProblem")

with open("data.json", "r") as f:
    data = json.load(f)

### Define the parameters

SedanCapacity = data["SedanCapacity"]
SedanPollution = data["SedanPollution"]
BusCapacity = data["BusCapacity"]
BusPollution = data["BusPollution"]
MaxPollution = data["MaxPollution"]
MinCustomers = data["MinCustomers"]

### Define the variables

SedanCount = model.addVar(vtype=GRB.INTEGER, name="SedanCount")
BusCount = model.addVar(vtype=GRB.INTEGER, name="BusCount")

### Define the constraints

model.addConstr(SedanPollution * SedanCount + BusPollution * BusCount <= MaxPollution)
model.addConstr(SedanCapacity * SedanCount + BusCapacity * BusCount >= MinCustomers)
model.addConstr(SedanCount >= 0)
model.addConstr(BusCount >= 0)

### Define the objective

model.setObjective(SedanCount + BusCount, GRB.MINIMIZE)

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