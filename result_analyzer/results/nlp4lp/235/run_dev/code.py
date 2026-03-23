
import os
import numpy as np
import json 
from gurobipy import Model, GRB, quicksum


model = Model("OptimizationProblem")

with open("data.json", "r") as f:
    data = json.load(f)




### Define the parameters

CapacityLarge = data["CapacityLarge"] # shape: [], definition: Capacity of a large cruise ship in number of customers

CapacitySmall = data["CapacitySmall"] # shape: [], definition: Capacity of a small cruise ship in number of customers

PollutionLarge = data["PollutionLarge"] # shape: [], definition: Pollution produced by a large cruise ship trip

PollutionSmall = data["PollutionSmall"] # shape: [], definition: Pollution produced by a small cruise ship trip

MaxLargeTrips = data["MaxLargeTrips"] # shape: [], definition: Maximum number of large cruise ship trips

MinSmallTripsPercentage = data["MinSmallTripsPercentage"] # shape: [], definition: Minimum proportion of total trips made by small cruise ships

RequiredCustomers = data["RequiredCustomers"] # shape: [], definition: Required number of customers to transport



### Define the variables

largeTrips = model.addVar(vtype=GRB.INTEGER, name="largeTrips")

smallTrips = model.addVar(vtype=GRB.INTEGER, name="smallTrips")



### Define the constraints

model.addConstr(largeTrips <= MaxLargeTrips)
model.addConstr(smallTrips >= MinSmallTripsPercentage * (largeTrips + smallTrips))
model.addConstr(CapacityLarge * largeTrips + CapacitySmall * smallTrips >= RequiredCustomers)
model.addConstr(largeTrips >= 0)
model.addConstr(smallTrips >= 0)


### Define the objective

model.setObjective(PollutionLarge * largeTrips + PollutionSmall * smallTrips, GRB.MINIMIZE)


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
