
import os
import numpy as np
import json 
from gurobipy import Model, GRB, quicksum


model = Model("OptimizationProblem")

with open("data.json", "r") as f:
    data = json.load(f)




### Define the parameters

TiresPerPlaneTrip = data["TiresPerPlaneTrip"] # shape: [], definition: Number of tires that can be transported by one cargo plane per trip

CostPerPlaneTrip = data["CostPerPlaneTrip"] # shape: [], definition: Cost of one cargo plane trip in dollars

TiresPerTruckTrip = data["TiresPerTruckTrip"] # shape: [], definition: Number of tires that can be transported by one ultrawide truck per trip

CostPerTruckTrip = data["CostPerTruckTrip"] # shape: [], definition: Cost of one ultrawide truck trip in dollars

MinTires = data["MinTires"] # shape: [], definition: Minimum number of tires to be transported

AvailableBudget = data["AvailableBudget"] # shape: [], definition: Available budget in dollars for transportation



### Define the variables

planeTrips = model.addVar(vtype=GRB.INTEGER, name="planeTrips")

truckTrips = model.addVar(vtype=GRB.INTEGER, name="truckTrips")



### Define the constraints

model.addConstr(TiresPerPlaneTrip * planeTrips + TiresPerTruckTrip * truckTrips >= MinTires)
model.addConstr(CostPerPlaneTrip * planeTrips + CostPerTruckTrip * truckTrips <= AvailableBudget)
model.addConstr(planeTrips <= truckTrips)
model.addConstr(planeTrips >= 0)
model.addConstr(truckTrips >= 0)


### Define the objective

model.setObjective(planeTrips + truckTrips, GRB.MINIMIZE)


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
