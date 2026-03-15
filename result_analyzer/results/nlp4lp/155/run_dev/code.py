
import os
import numpy as np
import json 
from gurobipy import Model, GRB, quicksum


model = Model("OptimizationProblem")

with open("data.json", "r") as f:
    data = json.load(f)




### Define the parameters

BikeCapacity = data["BikeCapacity"] # shape: [], definition: Number of meals a bike can hold

BikeCharge = data["BikeCharge"] # shape: [], definition: Units of charge a bike requires

ScooterCapacity = data["ScooterCapacity"] # shape: [], definition: Number of meals a scooter can hold

ScooterCharge = data["ScooterCharge"] # shape: [], definition: Units of charge a scooter requires

MaxBikeFraction = data["MaxBikeFraction"] # shape: [], definition: Maximum fraction of electric vehicles that can be bikes

MinScooters = data["MinScooters"] # shape: [], definition: Minimum number of scooters to be used

TotalCharge = data["TotalCharge"] # shape: [], definition: Total units of charge available



### Define the variables

numBikes = model.addVar(vtype=GRB.INTEGER, name="numBikes")

numScooters = model.addVar(vtype=GRB.INTEGER, name="numScooters")



### Define the constraints

model.addConstr(BikeCharge * numBikes + ScooterCharge * numScooters <= TotalCharge)
model.addConstr(7 * numBikes <= 3 * numScooters)
model.addConstr(numScooters >= MinScooters)
model.addConstr(numBikes >= 0)


### Define the objective

model.setObjective(BikeCapacity * numBikes + ScooterCapacity * numScooters, GRB.MAXIMIZE)


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
