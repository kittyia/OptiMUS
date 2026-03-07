
import os
import numpy as np
import json 
from gurobipy import Model, GRB, quicksum


model = Model("OptimizationProblem")

with open("data.json", "r") as f:
    data = json.load(f)




### Define the parameters

CarCapacity = data["CarCapacity"] # shape: [], definition: The number of employees that a car can take

CarPollution = data["CarPollution"] # shape: [], definition: The pollution produced by a car

BusCapacity = data["BusCapacity"] # shape: [], definition: The number of employees that a bus can take

BusPollution = data["BusPollution"] # shape: [], definition: The pollution produced by a bus

MinEmployeesToTransport = data["MinEmployeesToTransport"] # shape: [], definition: The minimum number of employees that need to be transported

MaxBuses = data["MaxBuses"] # shape: [], definition: The maximum number of buses that can be used



### Define the variables

Cars = model.addVar(vtype=GRB.INTEGER, name="Cars")

Buses = model.addVar(vtype=GRB.INTEGER, name="Buses")



### Define the constraints

model.addConstr(CarCapacity * Cars + BusCapacity * Buses >= MinEmployeesToTransport)
model.addConstr(Buses <= MaxBuses)
model.addConstr(Cars >= 0)
model.addConstr(Buses >= 0)


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
