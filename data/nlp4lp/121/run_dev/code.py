
import os
import numpy as np
import json 
from gurobipy import Model, GRB, quicksum


model = Model("OptimizationProblem")

with open("data.json", "r") as f:
    data = json.load(f)




### Define the parameters

CalorieBanana = data["CalorieBanana"] # shape: [], definition: Amount of calories per banana

CalorieMango = data["CalorieMango"] # shape: [], definition: Amount of calories per mango

PotassiumBanana = data["PotassiumBanana"] # shape: [], definition: Amount of potassium per banana

PotassiumMango = data["PotassiumMango"] # shape: [], definition: Amount of potassium per mango

SugarBanana = data["SugarBanana"] # shape: [], definition: Amount of sugar per banana

SugarMango = data["SugarMango"] # shape: [], definition: Amount of sugar per mango

MinCalories = data["MinCalories"] # shape: [], definition: Minimum total calories required

MinPotassium = data["MinPotassium"] # shape: [], definition: Minimum total potassium required

MaxMangoFraction = data["MaxMangoFraction"] # shape: [], definition: Maximum fraction of fruits that can be mangoes



### Define the variables

NumberOfBananas = model.addVar(vtype=GRB.INTEGER, name="NumberOfBananas")

NumberOfMangoes = model.addVar(vtype=GRB.INTEGER, name="NumberOfMangoes")



### Define the constraints

model.addConstr(CalorieBanana * NumberOfBananas + CalorieMango * NumberOfMangoes >= MinCalories)
model.addConstr(NumberOfMangoes <= MaxMangoFraction * (NumberOfBananas + NumberOfMangoes))
model.addConstr(NumberOfBananas >= 0)
model.addConstr(NumberOfMangoes >= 0)


### Define the objective

model.setObjective(SugarBanana * NumberOfBananas + SugarMango * NumberOfMangoes, GRB.MINIMIZE)


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
