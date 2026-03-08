
import os
import numpy as np
import json 
from gurobipy import Model, GRB, quicksum


model = Model("OptimizationProblem")

with open("data.json", "r") as f:
    data = json.load(f)




### Define the parameters

CapacityLarge = data["CapacityLarge"] # shape: [], definition: Number of cars a large plane can carry

CapacitySmall = data["CapacitySmall"] # shape: [], definition: Number of cars a small plane can carry

MinCars = data["MinCars"] # shape: [], definition: Minimum number of cars to deliver



### Define the variables

LargePlanes = model.addVar(vtype=GRB.INTEGER, name="LargePlanes")

SmallPlanes = model.addVar(vtype=GRB.INTEGER, name="SmallPlanes")



### Define the constraints

model.addConstr(CapacityLarge * LargePlanes + CapacitySmall * SmallPlanes >= MinCars)
model.addConstr(LargePlanes <= SmallPlanes - 1)
model.addConstr(LargePlanes >= 0)
model.addConstr(SmallPlanes >= 0)


### Define the objective

model.setObjective(LargePlanes + SmallPlanes, GRB.MINIMIZE)


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
