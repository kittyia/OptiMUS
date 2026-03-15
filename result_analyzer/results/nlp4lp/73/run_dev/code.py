
import os
import numpy as np
import json 
from gurobipy import Model, GRB, quicksum


model = Model("OptimizationProblem")

with open("data.json", "r") as f:
    data = json.load(f)




### Define the parameters

NumVehicleTypes = data["NumVehicleTypes"] # shape: [], definition: Number of vehicle types

MinLuggageRequired = data["MinLuggageRequired"] # shape: [], definition: Minimum number of luggage to move per day

MaxPollutantAllowed = data["MaxPollutantAllowed"] # shape: [], definition: Maximum pollutant allowed per day

LuggageCapacity = data["LuggageCapacity"] # shape: ['NumVehicleTypes'], definition: Luggage capacity per vehicle type per day

PollutantPerVehicleType = data["PollutantPerVehicleType"] # shape: ['NumVehicleTypes'], definition: Pollutant produced per vehicle type per day



### Define the variables

NumVehicles = model.addVars(NumVehicleTypes, vtype=GRB.INTEGER, name="NumVehicles")



### Define the constraints

model.addConstr(
    sum(LuggageCapacity[t] * NumVehicles[t] for t in range(NumVehicleTypes))
    >= MinLuggageRequired
)
model.addConstr(
    sum(PollutantPerVehicleType[i] * NumVehicles[i] for i in range(NumVehicleTypes))
    <= MaxPollutantAllowed
)
for i in range(NumVehicleTypes):
    model.addConstr(NumVehicles[i] >= 0)


### Define the objective

model.setObjective(quicksum(NumVehicles[i] for i in range(NumVehicleTypes)), GRB.MINIMIZE)


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
