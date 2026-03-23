
import os
import numpy as np
import json 
from gurobipy import Model, GRB, quicksum


model = Model("OptimizationProblem")

with open("data.json", "r") as f:
    data = json.load(f)




### Define the parameters

BusCapacity = data["BusCapacity"] # shape: [], definition: Number of chickens that a bus can carry per trip

BusTripTime = data["BusTripTime"] # shape: [], definition: Time taken by a bus per trip in hours

CarCapacity = data["CarCapacity"] # shape: [], definition: Number of chickens that a car can carry per trip

CarTripTime = data["CarTripTime"] # shape: [], definition: Time taken by a car per trip in hours

MaxBusTrips = data["MaxBusTrips"] # shape: [], definition: Maximum allowed number of bus trips

MinCarTripPercentage = data["MinCarTripPercentage"] # shape: [], definition: Minimum required percentage of total trips that must be by car

TotalChickens = data["TotalChickens"] # shape: [], definition: Total number of chickens that need to be transported



### Define the variables

BusTrips = model.addVar(vtype=GRB.INTEGER, name="BusTrips")

CarTrips = model.addVar(vtype=GRB.INTEGER, name="CarTrips")



### Define the constraints

model.addConstr(BusCapacity * BusTrips + CarCapacity * CarTrips >= TotalChickens)
model.addConstr(BusTrips <= MaxBusTrips)
model.addConstr(CarTrips >= MinCarTripPercentage * (BusTrips + CarTrips))
model.addConstr(BusTrips >= 0)
model.addConstr(CarTrips >= 0)


### Define the objective

model.setObjective(BusTripTime * BusTrips + CarTripTime * CarTrips, GRB.MINIMIZE)


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
