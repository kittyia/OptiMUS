
import os
import numpy as np
import json 
from gurobipy import Model, GRB, quicksum


model = Model("OptimizationProblem")

with open("data.json", "r") as f:
    data = json.load(f)




### Define the parameters

NumVehicleTypes = data["NumVehicleTypes"] # shape: [], definition: Number of vehicle types

Capacity = data["Capacity"] # shape: ['NumVehicleTypes'], definition: Capacity of each vehicle type in number of patties

CostPerTrip = data["CostPerTrip"] # shape: ['NumVehicleTypes'], definition: Cost per trip for each vehicle type

MinPatties = data["MinPatties"] # shape: [], definition: Minimum number of patties to be shipped

Budget = data["Budget"] # shape: [], definition: Budget for shipping



### Define the variables

Trips = model.addVars(NumVehicleTypes, vtype=GRB.INTEGER, name="Trips")



### Define the constraints

model.addConstr(
    sum(Capacity[v] * Trips[v] for v in range(NumVehicleTypes)) >= MinPatties
)
model.addConstr(
    sum(CostPerTrip[i] * Trips[i] for i in range(NumVehicleTypes)) <= Budget
)
model.addConstr(Trips[0] <= Trips[1])
for v in range(NumVehicleTypes):
    model.addConstr(Trips[v] >= 0)


### Define the objective

model.setObjective(quicksum(Trips[i] for i in range(NumVehicleTypes)), GRB.MINIMIZE)


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
