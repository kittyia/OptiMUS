
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

x = model.addVars(TotalTime + 1, vtype=GRB.CONTINUOUS, name="x")

v = model.addVars(TotalTime + 1, vtype=GRB.CONTINUOUS, name="v")

a = model.addVars(TotalTime, vtype=GRB.CONTINUOUS, name="a")



### Define the constraints

for t in range(TotalTime):
    model.addConstr(x[t+1] == x[t] + v[t])
for t in range(TotalTime):
    model.addConstr(v[t+1] == v[t] + a[t])
model.addConstr(x[0] == InitialPosition)
model.addConstr(v[0] == InitialVelocity)
model.addConstr(x[TotalTime] == FinalPosition)
model.addConstr(v[TotalTime] == FinalVelocity)


### Define the objective

Amax = model.addVar(name="Amax")

for t in range(TotalTime):
    model.addConstr(Amax >= a[t])
    model.addConstr(Amax >= -a[t])

model.setObjective(Amax, GRB.MINIMIZE)


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
