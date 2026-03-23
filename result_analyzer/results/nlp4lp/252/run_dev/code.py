
import os
import numpy as np
import json 
from gurobipy import Model, GRB, quicksum


model = Model("OptimizationProblem")

with open("data.json", "r") as f:
    data = json.load(f)




### Define the parameters

MinLocals = data["MinLocals"] # shape: [], definition: Minimum number of locals to transport

KayakCapacity = data["KayakCapacity"] # shape: [], definition: Number of people a kayak can transport per trip

MotorboatCapacity = data["MotorboatCapacity"] # shape: [], definition: Number of people a motorboat can transport per trip

KayakTime = data["KayakTime"] # shape: [], definition: Time in minutes a kayak takes per trip

MotorboatTime = data["MotorboatTime"] # shape: [], definition: Time in minutes a motorboat takes per trip

MaxMotorboatTrips = data["MaxMotorboatTrips"] # shape: [], definition: Maximum number of motorboat trips allowed

MinKayakTripPercentage = data["MinKayakTripPercentage"] # shape: [], definition: Minimum percentage of trips that must be by kayak



### Define the variables

KayakTrips = model.addVar(vtype=GRB.INTEGER, name="KayakTrips")

MotorboatTrips = model.addVar(vtype=GRB.INTEGER, name="MotorboatTrips")



### Define the constraints

model.addConstr(KayakCapacity * KayakTrips + MotorboatCapacity * MotorboatTrips >= MinLocals)
model.addConstr(MotorboatTrips <= MaxMotorboatTrips)
model.addConstr(KayakTrips >= 3 * MotorboatTrips)
model.addConstr(MotorboatTrips >= 0)
model.addConstr(KayakTrips >= 0)
model.addConstr(MotorboatTrips >= 0)


### Define the objective

model.setObjective(KayakTime * KayakTrips + MotorboatTime * MotorboatTrips, GRB.MINIMIZE)


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
