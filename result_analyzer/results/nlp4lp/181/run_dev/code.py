
import os
import numpy as np
import json 
from gurobipy import Model, GRB, quicksum


model = Model("OptimizationProblem")

with open("data.json", "r") as f:
    data = json.load(f)




### Define the parameters

TruckCapacity = data["TruckCapacity"] # shape: [], definition: Number of packages a truck can transport per trip

CarCapacity = data["CarCapacity"] # shape: [], definition: Number of packages a car can transport per trip

TruckGas = data["TruckGas"] # shape: [], definition: Liters of gas a truck uses per trip

CarGas = data["CarGas"] # shape: [], definition: Liters of gas a car uses per trip

MaxTruckTrips = data["MaxTruckTrips"] # shape: [], definition: Maximum number of truck trips allowed

MinCarTripPercentage = data["MinCarTripPercentage"] # shape: [], definition: Minimum percentage of trips that must be made by car

MinTotalPackages = data["MinTotalPackages"] # shape: [], definition: Minimum number of packages to transport



### Define the variables

TruckTrips = model.addVar(vtype=GRB.INTEGER, name="TruckTrips")

CarTrips = model.addVar(vtype=GRB.INTEGER, name="CarTrips")



### Define the constraints

model.addConstr(TruckCapacity * TruckTrips + CarCapacity * CarTrips >= MinTotalPackages)
model.addConstr(TruckTrips <= MaxTruckTrips)
model.addConstr(CarTrips >= (MinCarTripPercentage / 100) * (TruckTrips + CarTrips))
model.addConstr(TruckTrips >= 0)
model.addConstr(CarTrips >= 0)


### Define the objective

model.setObjective(TruckGas * TruckTrips + CarGas * CarTrips, GRB.MINIMIZE)


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
