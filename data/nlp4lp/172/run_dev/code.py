
import os
import numpy as np
import json 
from gurobipy import Model, GRB, quicksum


model = Model("OptimizationProblem")

with open("data.json", "r") as f:
    data = json.load(f)




### Define the parameters

HelicopterCapacity = data["HelicopterCapacity"] # shape: [], definition: Number of fish a helicopter can transport per trip

HelicopterTime = data["HelicopterTime"] # shape: [], definition: Time a helicopter takes per trip in minutes

CarCapacity = data["CarCapacity"] # shape: [], definition: Number of fish a car can transport per trip

CarTime = data["CarTime"] # shape: [], definition: Time a car takes per trip in minutes

MaxHelicopterTrips = data["MaxHelicopterTrips"] # shape: [], definition: Maximum number of helicopter trips allowed

MinPercentageCarTrips = data["MinPercentageCarTrips"] # shape: [], definition: Minimum percentage of trips that must be by car

MinFishToTransport = data["MinFishToTransport"] # shape: [], definition: Minimum number of fish to transport



### Define the variables

HelicopterTrips = model.addVar(vtype=GRB.INTEGER, name="HelicopterTrips")

CarTrips = model.addVar(vtype=GRB.INTEGER, name="CarTrips")



### Define the constraints

model.addConstr(
    HelicopterCapacity * HelicopterTrips + CarCapacity * CarTrips >= MinFishToTransport
)
model.addConstr(HelicopterTrips <= MaxHelicopterTrips)
model.addConstr(2 * CarTrips - 3 * HelicopterTrips >= 0)
model.addConstr(HelicopterTrips >= 0)
model.addConstr(CarTrips >= 0)
model.addConstr(HelicopterTrips >= 0)
model.addConstr(CarTrips >= 0)


### Define the objective




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
