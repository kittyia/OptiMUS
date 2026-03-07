
import os
import numpy as np
import json 
from gurobipy import Model, GRB, quicksum


model = Model("OptimizationProblem")

with open("data.json", "r") as f:
    data = json.load(f)




### Define the parameters

HotDogsPerSmallShop = data["HotDogsPerSmallShop"] # shape: [], definition: Number of hot dogs produced per small shop per day

WorkersPerSmallShop = data["WorkersPerSmallShop"] # shape: [], definition: Number of workers required for a small shop

HotDogsPerLargeShop = data["HotDogsPerLargeShop"] # shape: [], definition: Number of hot dogs produced per large shop per day

WorkersPerLargeShop = data["WorkersPerLargeShop"] # shape: [], definition: Number of workers required for a large shop

MinimumHotDogsPerDay = data["MinimumHotDogsPerDay"] # shape: [], definition: Minimum number of hot dogs to be produced per day

AvailableWorkers = data["AvailableWorkers"] # shape: [], definition: Total number of available workers



### Define the variables

SmallShops = model.addVar(vtype=GRB.INTEGER, name="SmallShops")

LargeShops = model.addVar(vtype=GRB.INTEGER, name="LargeShops")



### Define the constraints

model.addConstr(HotDogsPerSmallShop * SmallShops + HotDogsPerLargeShop * LargeShops >= MinimumHotDogsPerDay)
model.addConstr(WorkersPerSmallShop * SmallShops + WorkersPerLargeShop * LargeShops <= AvailableWorkers)
model.addConstr(SmallShops >= 0)
model.addConstr(LargeShops >= 0)


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
