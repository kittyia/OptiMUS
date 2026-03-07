
import os
import numpy as np
import json 
from gurobipy import Model, GRB, quicksum


model = Model("OptimizationProblem")

with open("data.json", "r") as f:
    data = json.load(f)




### Define the parameters

UnloadPersonsSmall = data["UnloadPersonsSmall"] # shape: [], definition: Number of persons required to unload a small container

CapacitySmall = data["CapacitySmall"] # shape: [], definition: Units of sand a small container can hold

UnloadPersonsLarge = data["UnloadPersonsLarge"] # shape: [], definition: Number of persons required to unload a large container

CapacityLarge = data["CapacityLarge"] # shape: [], definition: Units of sand a large container can hold

RatioSmallToLargeContainers = data["RatioSmallToLargeContainers"] # shape: [], definition: Required ratio of small containers to large containers

MinSmallContainers = data["MinSmallContainers"] # shape: [], definition: Minimum number of small containers to be used

MinLargeContainers = data["MinLargeContainers"] # shape: [], definition: Minimum number of large containers to be used

TotalPersonsAvailable = data["TotalPersonsAvailable"] # shape: [], definition: Total number of persons available



### Define the variables

SmallContainers = model.addVar(vtype=GRB.INTEGER, name="SmallContainers")

LargeContainers = model.addVar(vtype=GRB.INTEGER, name="LargeContainers")



### Define the constraints

model.addConstr(SmallContainers == RatioSmallToLargeContainers * LargeContainers)
model.addConstr(SmallContainers >= MinSmallContainers)
model.addConstr(LargeContainers >= MinLargeContainers)
model.addConstr(UnloadPersonsSmall * SmallContainers + UnloadPersonsLarge * LargeContainers <= TotalPersonsAvailable)


### Define the objective

model.setObjective(CapacitySmall * SmallContainers + CapacityLarge * LargeContainers, GRB.MAXIMIZE)


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
