import os
import numpy as np
import json
from gurobipy import Model, GRB, quicksum, abs_

model = Model("OptimizationProblem")

with open("data.json", "r") as f:
    data = json.load(f)

### Define the parameters

InitialPosition = data["InitialPosition"]
InitialVelocity = data["InitialVelocity"]
FinalPosition = data["FinalPosition"]
FinalVelocity = data["FinalVelocity"]
TotalTime = data["TotalTime"]

### Define the variables

position = model.addVars(TotalTime + 1, vtype=GRB.CONTINUOUS, name="position")
velocity = model.addVars(TotalTime + 1, vtype=GRB.CONTINUOUS, name="velocity")
acceleration = model.addVars(TotalTime, vtype=GRB.CONTINUOUS, name="acceleration")

### Define the constraints

for t in range(TotalTime):
    model.addConstr(position[t+1] == position[t] + velocity[t])

for t in range(TotalTime):
    model.addConstr(velocity[t+1] == velocity[t] + acceleration[t])

model.addConstr(position[0] == InitialPosition)
model.addConstr(velocity[0] == InitialVelocity)
model.addConstr(position[TotalTime] == FinalPosition)
model.addConstr(velocity[TotalTime] == FinalVelocity)

### Define the objective

model.setObjective(quicksum(abs_(acceleration[t]) for t in range(TotalTime)), GRB.MINIMIZE)

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