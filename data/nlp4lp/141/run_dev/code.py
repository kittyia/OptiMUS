
import os
import numpy as np
import json 
from gurobipy import Model, GRB, quicksum


model = Model("OptimizationProblem")

with open("data.json", "r") as f:
    data = json.load(f)




### Define the parameters

ShipCapacity = data["ShipCapacity"] # shape: [], definition: Capacity of a ship in containers

ShipFuel = data["ShipFuel"] # shape: [], definition: Fuel usage of a ship per trip in liters

PlaneCapacity = data["PlaneCapacity"] # shape: [], definition: Capacity of a plane in containers

PlaneFuel = data["PlaneFuel"] # shape: [], definition: Fuel usage of a plane per trip in liters

MinContainers = data["MinContainers"] # shape: [], definition: Minimum number of containers to transport

MaxPlaneTrips = data["MaxPlaneTrips"] # shape: [], definition: Maximum number of plane trips

MinShipTripFraction = data["MinShipTripFraction"] # shape: [], definition: Minimum fraction of trips that must be by ship



### Define the variables

ShipTrips = model.addVar(vtype=GRB.INTEGER, name="ShipTrips")

PlaneTrips = model.addVar(vtype=GRB.INTEGER, name="PlaneTrips")



### Define the constraints

model.addConstr(ShipCapacity * ShipTrips + PlaneCapacity * PlaneTrips >= MinContainers)
model.addConstr(PlaneTrips <= MaxPlaneTrips)
model.addConstr(ShipTrips >= PlaneTrips)
model.addConstr(PlaneTrips >= 0)



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
