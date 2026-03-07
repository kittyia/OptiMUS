
import os
import numpy as np
import json 
from gurobipy import Model, GRB, quicksum


model = Model("OptimizationProblem")

with open("data.json", "r") as f:
    data = json.load(f)




### Define the parameters

CostRice = data["CostRice"] # shape: [], definition: Cost per serving of Rice

CostKebab = data["CostKebab"] # shape: [], definition: Cost per serving of Kebab

CaloriesRice = data["CaloriesRice"] # shape: [], definition: Calories per serving of Rice

CaloriesKebab = data["CaloriesKebab"] # shape: [], definition: Calories per serving of Kebab

ProteinRice = data["ProteinRice"] # shape: [], definition: Protein per serving of Rice

ProteinKebab = data["ProteinKebab"] # shape: [], definition: Protein per serving of Kebab

MinCalories = data["MinCalories"] # shape: [], definition: Minimum daily calories required

MinProtein = data["MinProtein"] # shape: [], definition: Minimum daily protein required



### Define the variables

Rice = model.addVar(vtype=GRB.CONTINUOUS, name="Rice")

Kebab = model.addVar(vtype=GRB.CONTINUOUS, name="Kebab")



### Define the constraints

model.addConstr(CaloriesRice * Rice + CaloriesKebab * Kebab >= MinCalories)
model.addConstr(Rice >= 0)
model.addConstr(Kebab >= 0)


### Define the objective

model.setObjective(CostRice * Rice + CostKebab * Kebab, GRB.MINIMIZE)


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
