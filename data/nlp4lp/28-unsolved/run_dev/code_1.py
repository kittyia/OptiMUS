import os
import numpy as np
import json 
from gurobipy import Model, GRB, quicksum


model = Model("OptimizationProblem")

with open("data.json", "r") as f:
    data = json.load(f)

### Define the parameters

NumVitamins = data["NumVitamins"]
NumDrinks = data["NumDrinks"]
MinRequirements = data["MinRequirements"]
MaxRequirements = data["MaxRequirements"]
VitaminContent = data["VitaminContent"]

### Define the variables

xA = model.addVar(vtype=GRB.CONTINUOUS, name="xA", lb=0)
xB = model.addVar(vtype=GRB.CONTINUOUS, name="xB", lb=0)

### Define the constraints

model.addConstr(8 * xA + 15 * xB >= 150, name="VitaminA")
model.addConstr(6 * xA + 2 * xB >= 300, name="VitaminD")
model.addConstr(10 * xA + 20 * xB <= 400, name="VitaminE")

### Define the objective (Minimize Vitamin K)

model.setObjective(4 * xA + 12 * xB, GRB.MINIMIZE)

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