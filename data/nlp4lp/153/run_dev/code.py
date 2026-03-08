
import os
import numpy as np
import json 
from gurobipy import Model, GRB, quicksum


model = Model("OptimizationProblem")

with open("data.json", "r") as f:
    data = json.load(f)




### Define the parameters

TotalCows = data["TotalCows"] # shape: [], definition: The total number of cows that need to be transported

HelicopterCapacity = data["HelicopterCapacity"] # shape: [], definition: The number of cows that a helicopter can transport per trip

HelicopterPollution = data["HelicopterPollution"] # shape: [], definition: The amount of pollution created by a helicopter per trip

TruckCapacity = data["TruckCapacity"] # shape: [], definition: The number of cows that a truck can transport per trip

TruckPollution = data["TruckPollution"] # shape: [], definition: The amount of pollution created by a truck per trip

MaxTruckTrips = data["MaxTruckTrips"] # shape: [], definition: The maximum number of truck trips that can be made due to budget constraints



### Define the variables

HelicopterTrips = model.addVar(vtype=GRB.INTEGER, name="HelicopterTrips")

TruckTrips = model.addVar(vtype=GRB.INTEGER, name="TruckTrips")



### Define the constraints

model.addConstr(HelicopterCapacity * HelicopterTrips + TruckCapacity * TruckTrips >= TotalCows)
model.addConstr(TruckTrips >= 0)
model.addConstr(TruckTrips <= MaxTruckTrips)
model.addConstr(HelicopterTrips >= 0)


### Define the objective

model.setObjective(
    HelicopterPollution * HelicopterTrips + TruckPollution * TruckTrips,
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
