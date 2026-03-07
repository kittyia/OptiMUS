
import os
import numpy as np
import json 
from gurobipy import Model, GRB, quicksum


model = Model("OptimizationProblem")

with open("data.json", "r") as f:
    data = json.load(f)




### Define the parameters

TrainCapacity = data["TrainCapacity"] # shape: [], definition: Number of people transported per train per hour

TramCapacity = data["TramCapacity"] # shape: [], definition: Number of people transported per tram per hour

MinTramsToTrainsRatio = data["MinTramsToTrainsRatio"] # shape: [], definition: Minimum ratio of trams to trains

MinPeoplePerHour = data["MinPeoplePerHour"] # shape: [], definition: Minimum number of people to transport per hour



### Define the variables

TrainUnits = model.addVar(vtype=GRB.INTEGER, name="TrainUnits")

TramUnits = model.addVar(vtype=GRB.INTEGER, name="TramUnits")



### Define the constraints

model.addConstr(TrainCapacity * TrainUnits + TramCapacity * TramUnits >= MinPeoplePerHour)
model.addConstr(TramUnits >= MinTramsToTrainsRatio * TrainUnits)
model.addConstr(TrainUnits >= 0)
model.addConstr(TramUnits >= 0)


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
