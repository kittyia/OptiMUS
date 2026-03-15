
import os
import numpy as np
import json 
from gurobipy import Model, GRB, quicksum


model = Model("OptimizationProblem")

with open("data.json", "r") as f:
    data = json.load(f)




### Define the parameters

ProteinPerFishMeal = data["ProteinPerFishMeal"] # shape: [], definition: Protein per fish meal

ProteinPerChickenMeal = data["ProteinPerChickenMeal"] # shape: [], definition: Protein per chicken meal

IronPerFishMeal = data["IronPerFishMeal"] # shape: [], definition: Iron per fish meal

IronPerChickenMeal = data["IronPerChickenMeal"] # shape: [], definition: Iron per chicken meal

FatPerFishMeal = data["FatPerFishMeal"] # shape: [], definition: Fat per fish meal

FatPerChickenMeal = data["FatPerChickenMeal"] # shape: [], definition: Fat per chicken meal

MinimumProtein = data["MinimumProtein"] # shape: [], definition: Minimum required protein

MinimumIron = data["MinimumIron"] # shape: [], definition: Minimum required iron

ChickenToFishRatio = data["ChickenToFishRatio"] # shape: [], definition: Minimum ratio of chicken meals to fish meals



### Define the variables

FishMeals = model.addVar(vtype=GRB.INTEGER, name="FishMeals")

ChickenMeals = model.addVar(vtype=GRB.INTEGER, name="ChickenMeals")



### Define the constraints

model.addConstr(IronPerFishMeal * FishMeals + IronPerChickenMeal * ChickenMeals >= MinimumIron)
model.addConstr(ChickenMeals >= 2 * FishMeals)
model.addConstr(FishMeals >= 0)
model.addConstr(ChickenMeals >= 0)


### Define the objective

model.setObjective(FatPerFishMeal * FishMeals + FatPerChickenMeal * ChickenMeals, GRB.MINIMIZE)


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
