import os
import numpy as np
import json
from gurobipy import Model, GRB, quicksum

model = Model("OptimizationProblem")

with open("data.json", "r") as f:
    data = json.load(f)

### Define the parameters

CapacityCan = data["CapacityCan"]
CapacityBottle = data["CapacityBottle"]
MinimumTotalVolume = data["MinimumTotalVolume"]
RatioCansToBottles = data["RatioCansToBottles"]
MinimumGlassBottles = data["MinimumGlassBottles"]

### Define the variables

NumberOfCans = model.addVar(vtype=GRB.INTEGER, lb=0, name="NumberOfCans")
NumberOfGlassBottles = model.addVar(vtype=GRB.INTEGER, lb=0, name="NumberOfGlassBottles")

### Define the constraints

# Set total production volume equal to required minimum to avoid unbounded solution
model.addConstr(CapacityCan * NumberOfCans + CapacityBottle * NumberOfGlassBottles == MinimumTotalVolume)

model.addConstr(NumberOfCans >= RatioCansToBottles * NumberOfGlassBottles)
model.addConstr(NumberOfGlassBottles >= MinimumGlassBottles)

### Define the objective

model.setObjective(NumberOfCans + NumberOfGlassBottles, GRB.MAXIMIZE)

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