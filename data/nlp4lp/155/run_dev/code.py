
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

NumberOfBikes = model.addVar(vtype=GRB.INTEGER, name="NumberOfBikes")

NumberOfScooters = model.addVar(vtype=GRB.INTEGER, name="NumberOfScooters")



### Define the constraints

model.addConstr(BikeCharge * NumberOfBikes + ScooterCharge * NumberOfScooters <= TotalCharge)
model.addConstr(7 * NumberOfBikes <= 3 * NumberOfScooters)
model.addConstr(NumberOfScooters >= MinScooters)
model.addConstr(NumberOfBikes >= 0)
model.addConstr(NumberOfBikes >= 0)
model.addConstr(NumberOfScooters >= 0)


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
