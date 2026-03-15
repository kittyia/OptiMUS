
import os
import numpy as np
import json 
from gurobipy import Model, GRB, quicksum


model = Model("OptimizationProblem")

with open("data.json", "r") as f:
    data = json.load(f)




### Define the parameters

NumFoods = data["NumFoods"] # shape: [], definition: Number of food items

NumNutrients = data["NumNutrients"] # shape: [], definition: Number of nutrients

MinNutrient = data["MinNutrient"] # shape: ['NumNutrients'], definition: Minimum required amount for each nutrient

Price = data["Price"] # shape: ['NumFoods'], definition: Price of each food item

NutrientContent = data["NutrientContent"] # shape: ['NumNutrients', 'NumFoods'], definition: Amount of each nutrient in each food item



### Define the variables

FoodQuantity = model.addVars(NumFoods, vtype=GRB.CONTINUOUS, name="FoodQuantity")



### Define the constraints

model.addConstr(
    sum(NutrientContent[0][f] * FoodQuantity[f] for f in range(NumFoods)) >= 2200
)
model.addConstr(
    sum(NutrientContent[carbs_index][f] * FoodQuantity[f] for f in range(NumFoods)) >= 70
)
model.addConstr(FoodQuantity[1] >= 0)
model.addConstr(FoodQuantity[2] >= 0)


### Define the objective

model.setObjective(quicksum(Price[i] * FoodQuantity[i] for i in range(NumFoods)), GRB.MINIMIZE)


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
