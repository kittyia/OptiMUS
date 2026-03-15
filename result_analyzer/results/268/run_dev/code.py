
import os
import numpy as np
import json 
from gurobipy import Model, GRB, quicksum


model = Model("OptimizationProblem")

with open("data.json", "r") as f:
    data = json.load(f)




### Define the parameters

SedanCapacity = data["SedanCapacity"] # shape: [], definition: Number of tourists that a sedan can seat per day

SedanPollution = data["SedanPollution"] # shape: [], definition: Units of pollution resulting from one sedan per day

BusCapacity = data["BusCapacity"] # shape: [], definition: Number of tourists that a bus can seat per day

BusPollution = data["BusPollution"] # shape: [], definition: Units of pollution resulting from one bus per day

MaxPollution = data["MaxPollution"] # shape: [], definition: Maximum units of pollution allowed per day

MinCustomers = data["MinCustomers"] # shape: [], definition: Minimum number of customers required per day



### Define the variables

SedanCount = model.addVar(vtype=GRB.INTEGER, name="SedanCount")

BusCount = model.addVar(vtype=GRB.INTEGER, name="BusCount")



### Define the constraints

model.addConstr(SedanPollution * SedanCount + BusPollution * BusCount <= MaxPollution)
model.addConstr(SedanCapacity * SedanCount + BusCapacity * BusCount >= MinCustomers)
model.addConstr(SedanCount >= 0)
model.addConstr(BusCount >= 0)


### Define the objective

del.setObjective(SedanCount + BusCount, GRB.MINIMIZE


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
