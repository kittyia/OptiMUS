
import os
import numpy as np
import json 
from gurobipy import Model, GRB, quicksum


model = Model("OptimizationProblem")

with open("data.json", "r") as f:
    data = json.load(f)




### Define the parameters

VintageBottleCapacity = data["VintageBottleCapacity"] # shape: [], definition: Capacity of a vintage bottle in milliliters

RegularBottleCapacity = data["RegularBottleCapacity"] # shape: [], definition: Capacity of a regular bottle in milliliters

TotalAvailableVine = data["TotalAvailableVine"] # shape: [], definition: Total available vine in milliliters

RegularToVintageMinRatio = data["RegularToVintageMinRatio"] # shape: [], definition: Minimum ratio of regular bottles to vintage bottles

MinVintageBottles = data["MinVintageBottles"] # shape: [], definition: Minimum number of vintage bottles to be produced



### Define the variables

VintageBottles = model.addVar(vtype=GRB.INTEGER, name="VintageBottles")

RegularBottles = model.addVar(vtype=GRB.INTEGER, name="RegularBottles")



### Define the constraints

model.addConstr(VintageBottleCapacity * VintageBottles + RegularBottleCapacity * RegularBottles <= TotalAvailableVine)
model.addConstr(RegularBottles >= RegularToVintageMinRatio * VintageBottles)
model.addConstr(VintageBottles >= MinVintageBottles)



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
