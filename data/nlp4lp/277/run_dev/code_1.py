import os
import numpy as np
import json
from gurobipy import Model, GRB, quicksum


model = Model("OptimizationProblem")

with open("data.json", "r") as f:
    data = json.load(f)


# Define the parameters
InitialPosition = data["InitialPosition"]
InitialVelocity = data["InitialVelocity"]
FinalPosition = data["FinalPosition"]
FinalVelocity = data["FinalVelocity"]
TotalTime = data["TotalTime"]


# Define the variables
x = model.addVars(TotalTime + 1, vtype=GRB.CONTINUOUS, name="x")
v = model.addVars(TotalTime + 1, vtype=GRB.CONTINUOUS, name="v")
a = model.addVars(TotalTime, vtype=GRB.CONTINUOUS, name="a")


# Define the constraints
for t in range(TotalTime):
    model.addConstr(x[t+1] == x[t] + v[t])
    model.addConstr(v[t+1] == v[t] + a[t])

model.addConstr(x[0] == InitialPosition)
model.addConstr(v[0] == InitialVelocity)
model.addConstr(x[TotalTime] == FinalPosition)
model.addConstr(v[TotalTime] == FinalVelocity)


# Define the objective
Amax = model.addVar(vtype=GRB.CONTINUOUS, name="Amax")

for t in range(TotalTime):
    model.addConstr(Amax >= a[t])
    model.addConstr(Amax >= -a[t])

model.setObjective(Amax, GRB.MINIMIZE)


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