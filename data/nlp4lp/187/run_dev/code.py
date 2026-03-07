
import os
import numpy as np
import json 
from gurobipy import Model, GRB, quicksum


model = Model("OptimizationProblem")

with open("data.json", "r") as f:
    data = json.load(f)




### Define the parameters

CanoeCapacity = data["CanoeCapacity"] # shape: [], definition: Number of fish that a canoe can carry

DieselBoatCapacity = data["DieselBoatCapacity"] # shape: [], definition: Number of fish that a small diesel boat can carry

CanoeToBoatRatio = data["CanoeToBoatRatio"] # shape: [], definition: Minimum ratio of canoes to diesel boats

MinFish = data["MinFish"] # shape: [], definition: Minimum number of fish to be transported to shore



### Define the variables

Canoes = model.addVar(vtype=GRB.INTEGER, name="Canoes")

DieselBoats = model.addVar(vtype=GRB.INTEGER, name="DieselBoats")



### Define the constraints

model.addConstr(CanoeCapacity * Canoes + DieselBoatCapacity * DieselBoats >= MinFish)
model.addConstr(Canoes >= CanoeToBoatRatio * DieselBoats)
model.addConstr(DieselBoats >= 0)


### Define the objective

model.setObjective(Canoes + DieselBoats, GRB.MINIMIZE)


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
