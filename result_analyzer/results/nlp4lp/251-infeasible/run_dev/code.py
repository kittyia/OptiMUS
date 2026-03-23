
import os
import numpy as np
import json 
from gurobipy import Model, GRB, quicksum


model = Model("OptimizationProblem")

with open("data.json", "r") as f:
    data = json.load(f)




### Define the parameters

NumVehicleTypes = data["NumVehicleTypes"] # shape: [], definition: Number of different vehicle types.

TransportCapacity = data["TransportCapacity"] # shape: ['NumVehicleTypes'], definition: The number of people each vehicle type can transport per shift.

Pollution = data["Pollution"] # shape: ['NumVehicleTypes'], definition: The units of pollution each vehicle type produces per shift.

Earnings = data["Earnings"] # shape: ['NumVehicleTypes'], definition: The earnings the company makes per shift from each vehicle type.

MaxVehiclePercentage = data["MaxVehiclePercentage"] # shape: ['NumVehicleTypes'], definition: The maximum proportion of the total number of vehicles that can be of each vehicle type.

PollutionCap = data["PollutionCap"] # shape: [], definition: The maximum total units of pollution allowed per shift.

MinTransportCapacity = data["MinTransportCapacity"] # shape: [], definition: The minimum number of people that need to be transported per shift.



### Define the variables

NumVehicles = model.addVars(NumVehicleTypes, vtype=GRB.INTEGER, name="NumVehicles")



### Define the constraints

model.addConstr(
    sum(Pollution[i] * NumVehicles[i] for i in range(NumVehicleTypes)) <= PollutionCap
)
model.addConstr(
    sum(TransportCapacity[i] * NumVehicles[i] for i in range(NumVehicleTypes)) >= MinTransportCapacity
)
model.addConstr(NumVehicles[0] <= 0.25 * sum(NumVehicles[i] for i in range(NumVehicleTypes)))
for i in range(NumVehicleTypes):
    model.addConstr(NumVehicles[i] >= 0)


### Define the objective

model.setObjective(quicksum(Earnings[i] * NumVehicles[i] for i in range(NumVehicleTypes)), GRB.MAXIMIZE)


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
