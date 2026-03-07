
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

Bananas = model.addVar(vtype=GRB.INTEGER, name="Bananas")

Mangoes = model.addVar(vtype=GRB.INTEGER, name="Mangoes")



### Define the constraints

model.addConstr(CalorieBanana * Bananas + CalorieMango * Mangoes >= MinCalories)
model.addConstr(Mangoes <= MaxMangoFraction * (Bananas + Mangoes))
model.addConstr(Bananas >= 0)
model.addConstr(Mangoes >= 0)


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
