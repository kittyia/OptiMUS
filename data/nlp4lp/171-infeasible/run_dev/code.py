
import os
import numpy as np
import json 
from gurobipy import Model, GRB, quicksum


model = Model("OptimizationProblem")

with open("data.json", "r") as f:
    data = json.load(f)




### Define the parameters

SubmarineCapacity = data["SubmarineCapacity"] # shape: [], definition: Number of pieces of mail a submarine can carry per trip

SubmarineGasUsage = data["SubmarineGasUsage"] # shape: [], definition: Amount of gas a submarine uses per trip in liters

BoatCapacity = data["BoatCapacity"] # shape: [], definition: Number of pieces of mail a boat can carry per trip

BoatGasUsage = data["BoatGasUsage"] # shape: [], definition: Amount of gas a boat uses per trip in liters

MaxSubmarineTrips = data["MaxSubmarineTrips"] # shape: [], definition: Maximum number of submarine trips allowed

MinBoatTripPercentage = data["MinBoatTripPercentage"] # shape: [], definition: Minimum percentage of trips that must be by boat

MailRequired = data["MailRequired"] # shape: [], definition: Minimum number of pieces of mail to transport



### Define the variables

SubmarineTrips = model.addVar(vtype=GRB.INTEGER, name="SubmarineTrips")

BoatTrips = model.addVar(vtype=GRB.INTEGER, name="BoatTrips")



### Define the constraints

model.addConstr(SubmarineTrips <= MaxSubmarineTrips)
model.addConstr(100 * BoatTrips >= MinBoatTripPercentage * (SubmarineTrips + BoatTrips))
model.addConstr(SubmarineCapacity * SubmarineTrips + BoatCapacity * BoatTrips >= MailRequired)
model.addConstr(SubmarineTrips >= 0)
model.addConstr(BoatTrips >= 0)


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
