
import os
import numpy as np
import json 
from gurobipy import Model, GRB, quicksum


model = Model("OptimizationProblem")

with open("data.json", "r") as f:
    data = json.load(f)




### Define the parameters

NumSupplements = data["NumSupplements"] # shape: [], definition: Number of health supplements

NumNutrients = data["NumNutrients"] # shape: [], definition: Number of nutrients

AmountPerServing = data["AmountPerServing"] # shape: ['NumNutrients', 'NumSupplements'], definition: Amount of nutrient i per serving of supplement j

CostPerServing = data["CostPerServing"] # shape: ['NumSupplements'], definition: Cost per serving of supplement j

MinimumRequirement = data["MinimumRequirement"] # shape: ['NumNutrients'], definition: Minimum required amount of nutrient i



### Define the variables

Servings = model.addVars(NumSupplements, vtype=GRB.CONTINUOUS, name="Servings")



### Define the constraints

model.addConstr(
    sum(AmountPerServing[0][j] * Servings[j] for j in range(NumSupplements)) 
    >= MinimumRequirement[0]
)
model.addConstr(Servings[1] >= 0)
model.addConstr(Servings[1] >= 0)


### Define the objective

model.setObjective(quicksum(CostPerServing[j] * Servings[j] for j in range(NumSupplements)), GRB.MINIMIZE)


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
