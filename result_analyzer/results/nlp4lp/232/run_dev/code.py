
import os
import numpy as np
import json 
from gurobipy import Model, GRB, quicksum


model = Model("OptimizationProblem")

with open("data.json", "r") as f:
    data = json.load(f)




### Define the parameters

NumFoodTypes = data["NumFoodTypes"] # shape: [], definition: Number of food types

CaloriePerBowl = data["CaloriePerBowl"] # shape: ['NumFoodTypes'], definition: Calorie content per bowl for each food type

ProteinPerBowl = data["ProteinPerBowl"] # shape: ['NumFoodTypes'], definition: Protein content per bowl for each food type

SodiumPerBowl = data["SodiumPerBowl"] # shape: ['NumFoodTypes'], definition: Sodium content per bowl for each food type

MaxMealProportionEggs = data["MaxMealProportionEggs"] # shape: [], definition: Maximum proportion of meals that can be eggs

MinCalories = data["MinCalories"] # shape: [], definition: Minimum total calories required

MinProtein = data["MinProtein"] # shape: [], definition: Minimum total protein required



### Define the variables

NumBowls = model.addVars(NumFoodTypes, vtype=GRB.INTEGER, name="NumBowls")



### Define the constraints

model.addConstr(
    sum(CaloriePerBowl[i] * NumBowls[i] for i in range(NumFoodTypes)) >= MinCalories
)
model.addConstr(
    sum(ProteinPerBowl[i] * NumBowls[i] for i in range(NumFoodTypes)) >= MinProtein
)
model.addConstr(
    NumBowls[1] <= MaxMealProportionEggs * sum(NumBowls[f] for f in range(NumFoodTypes))
)
model.addConstr(NumBowls[1] >= 0)
model.addConstr(NumBowls[1] >= 0)


### Define the objective

model.setObjective(quicksum(SodiumPerBowl[i] * NumBowls[i] for i in range(NumFoodTypes)), GRB.MINIMIZE)


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
