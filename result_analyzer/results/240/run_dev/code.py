
import os
import numpy as np
import json 
from gurobipy import Model, GRB, quicksum


model = Model("OptimizationProblem")

with open("data.json", "r") as f:
    data = json.load(f)




### Define the parameters

CapacityCan = data["CapacityCan"] # shape: [], definition: The amount of soda that one can container holds, in milliliters.

CapacityBottle = data["CapacityBottle"] # shape: [], definition: The amount of soda that one glass bottle container holds, in milliliters.

MinimumTotalVolume = data["MinimumTotalVolume"] # shape: [], definition: The minimum total volume of soda that needs to be bottled each day, in milliliters.

RatioCansToBottles = data["RatioCansToBottles"] # shape: [], definition: The minimum ratio of number of cans to number of glass bottles.

MinimumGlassBottles = data["MinimumGlassBottles"] # shape: [], definition: The minimum number of glass bottles that must be produced.



### Define the variables

NumCans = model.addVar(vtype=GRB.INTEGER, name="NumCans")

NumGlassBottles = model.addVar(vtype=GRB.INTEGER, name="NumGlassBottles")



### Define the constraints

model.addConstr(CapacityCan * NumCans + CapacityBottle * NumGlassBottles >= MinimumTotalVolume)
model.addConstr(NumCans >= RatioCansToBottles * NumGlassBottles)
model.addConstr(NumGlassBottles >= MinimumGlassBottles)


### Define the objective

model.setObjective(NumCans + NumGlassBottles, GRB.MAXIMIZE)


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
