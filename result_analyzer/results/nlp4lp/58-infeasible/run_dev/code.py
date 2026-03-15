
import os
import numpy as np
import json 
from gurobipy import Model, GRB, quicksum


model = Model("OptimizationProblem")

with open("data.json", "r") as f:
    data = json.load(f)




### Define the parameters

KidsBottleCapacity = data["KidsBottleCapacity"] # shape: [], definition: Capacity of a kids size bottle in milliliters

AdultBottleCapacity = data["AdultBottleCapacity"] # shape: [], definition: Capacity of an adult size bottle in milliliters

AdultToKidsRatio = data["AdultToKidsRatio"] # shape: [], definition: Minimum ratio of adult bottles to kids bottles

MinKidsBottles = data["MinKidsBottles"] # shape: [], definition: Minimum number of kids size bottles to be produced

AvailableSyrup = data["AvailableSyrup"] # shape: [], definition: Total available milliliters of cough syrup



### Define the variables

KidsBottles = model.addVar(vtype=GRB.INTEGER, name="KidsBottles")

AdultBottles = model.addVar(vtype=GRB.INTEGER, name="AdultBottles")



### Define the constraints

model.addConstr(KidsBottleCapacity * KidsBottles + AdultBottleCapacity * AdultBottles <= AvailableSyrup)
model.addConstr(AdultBottles >= AdultToKidsRatio * KidsBottles)
model.addConstr(KidsBottles >= MinKidsBottles)
model.addConstr(KidsBottles >= 0)
model.addConstr(AdultBottles >= 0)


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
