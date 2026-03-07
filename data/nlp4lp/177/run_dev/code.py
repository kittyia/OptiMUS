
import os
import numpy as np
import json 
from gurobipy import Model, GRB, quicksum


model = Model("OptimizationProblem")

with open("data.json", "r") as f:
    data = json.load(f)




### Define the parameters

FerryTripCapacity = data["FerryTripCapacity"] # shape: [], definition: Number of boxes of corn that can be sent per ferry trip

LightRailTripCapacity = data["LightRailTripCapacity"] # shape: [], definition: Number of boxes of corn that can be sent per light rail trip

MinLightRailMultiplier = data["MinLightRailMultiplier"] # shape: [], definition: Minimum multiple that the number of light rail trips must be compared to ferry trips

MinBoxesToSend = data["MinBoxesToSend"] # shape: [], definition: Minimum number of boxes of corn that the farmer wants to send



### Define the variables

FerryTrips = model.addVar(vtype=GRB.INTEGER, name="FerryTrips")

LightRailTrips = model.addVar(vtype=GRB.INTEGER, name="LightRailTrips")



### Define the constraints

model.addConstr(FerryTripCapacity * FerryTrips + LightRailTripCapacity * LightRailTrips >= MinBoxesToSend)
model.addConstr(LightRailTrips >= MinLightRailMultiplier * FerryTrips)
model.addConstr(FerryTrips >= 0)
model.addConstr(LightRailTrips >= 0)


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
