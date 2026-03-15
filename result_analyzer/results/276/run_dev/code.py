
import os
import numpy as np
import json 
from gurobipy import Model, GRB, quicksum


model = Model("OptimizationProblem")

with open("data.json", "r") as f:
    data = json.load(f)




### Define the parameters

InitialPosition = data["InitialPosition"] # shape: [], definition: Initial position of the rocket

InitialVelocity = data["InitialVelocity"] # shape: [], definition: Initial velocity of the rocket

FinalPosition = data["FinalPosition"] # shape: [], definition: Target final position of the rocket

FinalVelocity = data["FinalVelocity"] # shape: [], definition: Target final velocity of the rocket

TotalTime = data["TotalTime"] # shape: [], definition: Total number of time steps



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

print("Optimal Objective Value: ", model.objVal)


if model.status == GRB.OPTIMAL:
    with open("output_solution.txt", "w") as f:
        f.write(str(model.objVal))
    print("Optimal Objective Value: ", model.objVal)
else:
    with open("output_solution.txt", "w") as f:
        f.write(model.status)
