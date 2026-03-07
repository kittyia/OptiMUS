
import os
import numpy as np
import json 
from gurobipy import Model, GRB, quicksum


model = Model("OptimizationProblem")

with open("data.json", "r") as f:
    data = json.load(f)




### Define the parameters

TotalMonkeys = data["TotalMonkeys"] # shape: [], definition: Number of monkeys to transport

BusCapacity = data["BusCapacity"] # shape: [], definition: Number of monkeys a bus can transport per trip

BusTripTime = data["BusTripTime"] # shape: [], definition: Time in minutes a bus takes per trip

CarCapacity = data["CarCapacity"] # shape: [], definition: Number of monkeys a car can transport per trip

CarTripTime = data["CarTripTime"] # shape: [], definition: Time in minutes a car takes per trip

MaxBusTrips = data["MaxBusTrips"] # shape: [], definition: Maximum number of bus trips allowed

MinCarTripFraction = data["MinCarTripFraction"] # shape: [], definition: Minimum fraction of trips that must be by car



### Define the variables

BusTrips = model.addVar(vtype=GRB.INTEGER, name="BusTrips")

CarTrips = model.addVar(vtype=GRB.INTEGER, name="CarTrips")



### Define the constraints

model.addConstr(BusCapacity * BusTrips + CarCapacity * CarTrips >= TotalMonkeys)
model.addConstr(BusTrips <= MaxBusTrips)
model.addConstr(2 * CarTrips >= 3 * BusTrips)
model.addConstr(BusTrips >= 0)
model.addConstr(CarTrips >= 0)
model.addConstr(BusTrips >= 0)
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
