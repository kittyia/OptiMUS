
import os
import numpy as np
import json 
from gurobipy import Model, GRB, quicksum


model = Model("OptimizationProblem")

with open("data.json", "r") as f:
    data = json.load(f)




### Define the parameters

HelicopterCapacity = data["HelicopterCapacity"] # shape: [], definition: Number of patients that can be transported by helicopter in one trip

HelicopterTripTime = data["HelicopterTripTime"] # shape: [], definition: Time taken for one helicopter trip

BusCapacity = data["BusCapacity"] # shape: [], definition: Number of patients that can be transported by bus in one trip

BusTripTime = data["BusTripTime"] # shape: [], definition: Time taken for one bus trip

MinPatients = data["MinPatients"] # shape: [], definition: Minimum number of patients that need to be transported

MinHelicopterTripPercentage = data["MinHelicopterTripPercentage"] # shape: [], definition: Minimum percentage of trips that should be by helicopter

MaxBusTrips = data["MaxBusTrips"] # shape: [], definition: Maximum number of bus trips allowed



### Define the variables

HelicopterTrips = model.addVar(vtype=GRB.INTEGER, name="HelicopterTrips")

BusTrips = model.addVar(vtype=GRB.INTEGER, name="BusTrips")



### Define the constraints

model.addConstr(HelicopterCapacity * HelicopterTrips + BusCapacity * BusTrips >= MinPatients)
model.addConstr(7 * HelicopterTrips - 3 * BusTrips >= 0)
model.addConstr(BusTrips <= MaxBusTrips)
model.addConstr(HelicopterTrips >= 0)
model.addConstr(BusTrips >= 0)


### Define the objective

model.setObjective(
    HelicopterTripTime * HelicopterTrips + BusTripTime * BusTrips,
    GRB.MINIMIZE
)


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
