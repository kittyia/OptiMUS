
import os
import numpy as np
import json 
from gurobipy import Model, GRB, quicksum


model = Model("OptimizationProblem")

with open("data.json", "r") as f:
    data = json.load(f)




### Define the parameters

VegetableVitamins = data["VegetableVitamins"] # shape: [], definition: Amount of vitamins in one serving of vegetables

VegetableMinerals = data["VegetableMinerals"] # shape: [], definition: Amount of minerals in one serving of vegetables

FruitVitamins = data["FruitVitamins"] # shape: [], definition: Amount of vitamins in one serving of fruits

FruitMinerals = data["FruitMinerals"] # shape: [], definition: Amount of minerals in one serving of fruits

MinimumVitamins = data["MinimumVitamins"] # shape: [], definition: Minimum required units of vitamins

MinimumMinerals = data["MinimumMinerals"] # shape: [], definition: Minimum required units of minerals

VegetableCost = data["VegetableCost"] # shape: [], definition: Cost per serving of vegetables

FruitCost = data["FruitCost"] # shape: [], definition: Cost per serving of fruits



### Define the variables

VegetableServings = model.addVar(vtype=GRB.CONTINUOUS, name="VegetableServings")

FruitServings = model.addVar(vtype=GRB.CONTINUOUS, name="FruitServings")



### Define the constraints

model.addConstr(VegetableVitamins * VegetableServings + FruitVitamins * FruitServings >= MinimumVitamins)
model.addConstr(3 * VegetableServings + 1 * FruitServings >= 30)
model.addConstr(VegetableServings >= 0)
model.addConstr(FruitServings >= 0)


### Define the objective

del.setObjective(VegetableCost * VegetableServings + FruitCost * FruitServings, GRB.MINIMIZE


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
