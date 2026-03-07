
import os
import numpy as np
import json 
from gurobipy import Model, GRB, quicksum


model = Model("OptimizationProblem")

with open("data.json", "r") as f:
    data = json.load(f)




### Define the parameters

BoatCapacity = data["BoatCapacity"] # shape: [], definition: Number of ducks a boat can carry per trip

CanoeCapacity = data["CanoeCapacity"] # shape: [], definition: Number of ducks a canoe can carry per trip

BoatTripTime = data["BoatTripTime"] # shape: [], definition: Time in minutes per boat trip

CanoeTripTime = data["CanoeTripTime"] # shape: [], definition: Time in minutes per canoe trip

MaxBoatTrips = data["MaxBoatTrips"] # shape: [], definition: Maximum number of boat trips allowed

MinCanoeTripFraction = data["MinCanoeTripFraction"] # shape: [], definition: Minimum fraction of trips that must be by canoe

MinDucks = data["MinDucks"] # shape: [], definition: Minimum number of ducks to be transported to shore



### Define the variables

BoatTrips = model.addVar(vtype=GRB.INTEGER, name="BoatTrips")

CanoeTrips = model.addVar(vtype=GRB.INTEGER, name="CanoeTrips")



### Define the constraints

model.addConstr(BoatTrips >= 0)
model.addConstr(CanoeTrips >= 0)
model.addConstr(BoatTrips <= MaxBoatTrips)
model.addConstr(CanoeTrips >= MinCanoeTripFraction * (BoatTrips + CanoeTrips))
model.addConstr(BoatCapacity * BoatTrips + CanoeCapacity * CanoeTrips >= MinDucks)


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
