
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

Position = model.addVars(TotalTime+1, vtype=GRB.CONTINUOUS, name="Position")

Velocity = model.addVars(TotalTime+1, vtype=GRB.CONTINUOUS, name="Velocity")

Acceleration = model.addVars(TotalTime, vtype=GRB.CONTINUOUS, name="Acceleration")



### Define the constraints

for t in range(TotalTime):
    model.addConstr(Position[t+1] == Position[t] + Velocity[t])
for t in range(TotalTime):
    model.addConstr(Velocity[t+1] == Velocity[t] + Acceleration[t])
model.addConstr(Position[0] == InitialPosition)
model.addConstr(Velocity[0] == InitialVelocity)
model.addConstr(Position[TotalTime] == FinalPosition)
model.addConstr(Velocity[TotalTime] == FinalVelocity)


### Define the objective

max_thrust = model.addVar(vtype=GRB.CONTINUOUS, name="max_thrust")

for t in range(TotalTime):
    model.addConstr(max_thrust >= Acceleration[t])
    model.addConstr(max_thrust >= -Acceleration[t])

model.setObjective(max_thrust, GRB.MINIMIZE)


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
