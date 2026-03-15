
import os
import numpy as np
import json 
from gurobipy import Model, GRB, quicksum


model = Model("OptimizationProblem")

with open("data.json", "r") as f:
    data = json.load(f)




### Define the parameters

BusCapacity = data["BusCapacity"] # shape: [], definition: BusCapacity

CarCapacity = data["CarCapacity"] # shape: [], definition: CarCapacity

MinChildren = data["MinChildren"] # shape: [], definition: MinChildren

MinCars = data["MinCars"] # shape: [], definition: MinCars



### Define the variables

NumBuses = model.addVar(vtype=GRB.INTEGER, name="NumBuses")

NumCars = model.addVar(vtype=GRB.INTEGER, name="NumCars")



### Define the constraints

model.addConstr(BusCapacity * NumBuses + CarCapacity * NumCars >= MinChildren)
model.addConstr(NumBuses >= NumCars + 1)
model.addConstr(NumCars >= MinCars)
model.addConstr(NumBuses >= 0)
model.addConstr(NumCars >= 0)


### Define the objective

model.setObjective(NumBuses + NumCars, GRB.MINIMIZE)


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
