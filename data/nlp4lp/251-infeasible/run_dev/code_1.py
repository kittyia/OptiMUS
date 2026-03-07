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

# At most 25% (or given percentage) of total vehicles can be of each type (as specified)
model.addConstr(
    NumVehicles[0] <= MaxVehiclePercentage[0] *
    quicksum(NumVehicles[t] for t in range(NumVehicleTypes))
)

# Pollution constraint
model.addConstr(
    quicksum(Pollution[i] * NumVehicles[i] for i in range(NumVehicleTypes)) <= PollutionCap
)

# Minimum transport capacity constraint
model.addConstr(
    quicksum(TransportCapacity[i] * NumVehicles[i] for i in range(NumVehicleTypes))
    >= MinTransportCapacity
)

# Non-negativity (redundant since INTEGER defaults to lb=0, but kept for clarity)
for i in range(NumVehicleTypes):
    model.addConstr(NumVehicles[i] >= 0)


### Define the objective (maximize earnings)

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