
import os
import numpy as np
import json 
from gurobipy import Model, GRB, quicksum


model = Model("OptimizationProblem")

with open("data.json", "r") as f:
    data = json.load(f)




### Define the parameters

NewCompanyCapacity = data["NewCompanyCapacity"] # shape: [], definition: Delivery capacity per trip of the new shipping company

OldCompanyCapacity = data["OldCompanyCapacity"] # shape: [], definition: Delivery capacity per trip of the old shipping company

NewCompanyDiesel = data["NewCompanyDiesel"] # shape: [], definition: Diesel consumption per trip of the new shipping company

OldCompanyDiesel = data["OldCompanyDiesel"] # shape: [], definition: Diesel consumption per trip of the old shipping company

MinimumGifts = data["MinimumGifts"] # shape: [], definition: Minimum number of gifts to deliver

MaxTripsNewCompany = data["MaxTripsNewCompany"] # shape: [], definition: Maximum number of trips by the new shipping company

MinimumOldCompanyTripPercentage = data["MinimumOldCompanyTripPercentage"] # shape: [], definition: Minimum percentage of trips that must be made by the old shipping company



### Define the variables

NewTrips = model.addVar(vtype=GRB.INTEGER, name="NewTrips")

OldTrips = model.addVar(vtype=GRB.INTEGER, name="OldTrips")



### Define the constraints

model.addConstr(NewCompanyCapacity * NewTrips + OldCompanyCapacity * OldTrips >= MinimumGifts)
model.addConstr(NewTrips <= MaxTripsNewCompany)
model.addConstr(3 * OldTrips >= 2 * NewTrips)
model.addConstr(NewTrips >= 0)
model.addConstr(NewTrips >= 0)
model.addConstr(OldTrips >= 0)


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
