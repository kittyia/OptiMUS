
import os
import numpy as np
import json 
from gurobipy import Model, GRB, quicksum


model = Model("OptimizationProblem")

with open("data.json", "r") as f:
    data = json.load(f)




### Define the parameters

NumDessertTypes = data["NumDessertTypes"] # shape: [], definition: Number of different dessert types

NumIngredients = data["NumIngredients"] # shape: [], definition: Number of different ingredients

ResourceUsage = data["ResourceUsage"] # shape: ['NumIngredients', 'NumDessertTypes'], definition: Amount of each ingredient required to produce one unit of each dessert

AvailableIngredients = data["AvailableIngredients"] # shape: ['NumIngredients'], definition: Total available units of each ingredient

MinMatchaProportion = data["MinMatchaProportion"] # shape: [], definition: Minimum proportion of desserts that must be matcha ice cream



### Define the variables

MatchaQuantity = model.addVar(vtype=GRB.CONTINUOUS, name="MatchaQuantity")

OrangeQuantity = model.addVar(vtype=GRB.CONTINUOUS, name="OrangeQuantity")



### Define the constraints

model.addConstr(4 * MatchaQuantity <= 600)
model.addConstr(3 * OrangeQuantity <= 550)
model.addConstr(OrangeQuantity >= MatchaQuantity)
model.addConstr(MatchaQuantity >= MinMatchaProportion * (MatchaQuantity + OrangeQuantity))
model.addConstr(MatchaQuantity >= 0)
model.addConstr(OrangeQuantity >= 0)


### Define the objective

model.setObjective(2 * MatchaQuantity + 4 * OrangeQuantity, GRB.MINIMIZE)


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
