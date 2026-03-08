import os
import numpy as np
import json 
from gurobipy import Model, GRB, quicksum


model = Model("OptimizationProblem")

with open("data.json", "r") as f:
    data = json.load(f)


### Define the parameters

NumVehicleTypes = data["NumVehicleTypes"]

TransportCapacity = data["TransportCapacity"]

Pollution = data["Pollution"]

Earnings = data["Earnings"]

MaxVehiclePercentage = data["MaxVehiclePercentage"]

PollutionCap = data["PollutionCap"]

MinTransportCapacity = data["MinTransportCapacity"]


### Define the variables

NumVehicles = model.addVars(NumVehicleTypes, vtype=GRB.INTEGER, name="NumVehicles")


### Define the constraints

model.addConstr(
    quicksum(Pollution[i] * NumVehicles[i] for i in range(NumVehicleTypes)) <= PollutionCap
)

model.addConstr(
    quicksum(TransportCapacity[i] * NumVehicles[i] for i in range(NumVehicleTypes)) >= MinTransportCapacity
)

# At most 25% of vehicles can be motorcycles (assumed index 0)
model.addConstr(
    NumVehicles[0] <= 0.25 * quicksum(NumVehicles[i] for i in range(NumVehicleTypes))
)

for i in range(NumVehicleTypes):
    model.addConstr(NumVehicles[i] >= 0)


### Define the objective

model.setObjective(
    quicksum(Earnings[i] * NumVehicles[i] for i in range(NumVehicleTypes)),
    GRB.MAXIMIZE
)


### Optimize the model

model.optimize()


### Output optimal objective value

if model.status == GRB.OPTIMAL:
    print("Optimal Objective Value: ", model.ObjVal)
    with open("output_solution.txt", "w") as f:
        f.write(str(model.ObjVal))
else:
    with open("output_solution.txt", "w") as f:
        f.write(str(model.status))