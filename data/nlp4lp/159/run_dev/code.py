
import os
import numpy as np
import json 
from gurobipy import Model, GRB, quicksum


model = Model("OptimizationProblem")

with open("data.json", "r") as f:
    data = json.load(f)




### Define the parameters

CamelCapacity = data["CamelCapacity"] # shape: [], definition: Number of packages a camel can carry

HorseCapacity = data["HorseCapacity"] # shape: [], definition: Number of packages a horse can carry

CamelFood = data["CamelFood"] # shape: [], definition: Units of food a camel requires

HorseFood = data["HorseFood"] # shape: [], definition: Units of food a horse requires

MinPackages = data["MinPackages"] # shape: [], definition: Minimum number of packages to be delivered

FoodAvailable = data["FoodAvailable"] # shape: [], definition: Total units of food available



### Define the variables

CamelCount = model.addVar(vtype=GRB.INTEGER, name="CamelCount")

HorseCount = model.addVar(vtype=GRB.INTEGER, name="HorseCount")



### Define the constraints

model.addConstr(CamelCapacity * CamelCount + HorseCapacity * HorseCount >= MinPackages)
model.addConstr(CamelFood * CamelCount + HorseFood * HorseCount <= FoodAvailable)
model.addConstr(HorseCount <= CamelCount)
model.addConstr(CamelCount >= 0)
model.addConstr(HorseCount >= 0)


### Define the objective

model.setObjective(CamelCount + HorseCount, GRB.MINIMIZE)


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
