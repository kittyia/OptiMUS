
import os
import numpy as np
import json 
from gurobipy import Model, GRB, quicksum


model = Model("OptimizationProblem")

with open("data.json", "r") as f:
    data = json.load(f)




### Define the parameters

GlassBottleCapacity = data["GlassBottleCapacity"] # shape: [], definition: The capacity of a glass bottle in milliliters

PlasticBottleCapacity = data["PlasticBottleCapacity"] # shape: [], definition: The capacity of a plastic bottle in milliliters

MinPlasticRatio = data["MinPlasticRatio"] # shape: [], definition: The minimum ratio of plastic bottles to glass bottles

MinGlassBottles = data["MinGlassBottles"] # shape: [], definition: The minimum number of glass bottles required

TotalWater = data["TotalWater"] # shape: [], definition: Total volume of water available in milliliters



### Define the variables

GlassBottles = model.addVar(vtype=GRB.INTEGER, name="GlassBottles")

PlasticBottles = model.addVar(vtype=GRB.INTEGER, name="PlasticBottles")



### Define the constraints

model.addConstr(GlassBottleCapacity * GlassBottles + PlasticBottleCapacity * PlasticBottles <= TotalWater)
model.addConstr(PlasticBottles >= MinPlasticRatio * GlassBottles)
model.addConstr(GlassBottles >= MinGlassBottles)
model.addConstr(GlassBottles >= 0)
model.addConstr(PlasticBottles >= 0)


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
