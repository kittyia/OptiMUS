
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

busTrips = model.addVar(vtype=GRB.INTEGER, name="busTrips")

carTrips = model.addVar(vtype=GRB.INTEGER, name="carTrips")



### Define the constraints

model.addConstr(BusCapacity * busTrips + CarCapacity * carTrips >= TotalChickens)
model.addConstr(busTrips <= MaxBusTrips)
model.addConstr(carTrips >= 1.5 * busTrips)
model.addConstr(busTrips >= 0)
# No additional constraints are needed here because integrality
# is enforced when defining the variables with vtype=GRB.INTEGER.


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
