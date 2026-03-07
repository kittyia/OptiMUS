
import os
import numpy as np
import json 
from gurobipy import Model, GRB, quicksum


model = Model("OptimizationProblem")

with open("data.json", "r") as f:
    data = json.load(f)




### Define the parameters

CaloriesPerRamenPack = data["CaloriesPerRamenPack"] # shape: [], definition: Calories per pack of ramen

ProteinPerRamenPack = data["ProteinPerRamenPack"] # shape: [], definition: Protein per pack of ramen

SodiumPerRamenPack = data["SodiumPerRamenPack"] # shape: [], definition: Sodium per pack of ramen

CaloriesPerFriesPack = data["CaloriesPerFriesPack"] # shape: [], definition: Calories per pack of fries

ProteinPerFriesPack = data["ProteinPerFriesPack"] # shape: [], definition: Protein per pack of fries

SodiumPerFriesPack = data["SodiumPerFriesPack"] # shape: [], definition: Sodium per pack of fries

MaxRamenMealRatio = data["MaxRamenMealRatio"] # shape: [], definition: Maximum proportion of meals that can be ramen

MinCalories = data["MinCalories"] # shape: [], definition: Minimum calories required

MinProtein = data["MinProtein"] # shape: [], definition: Minimum protein required



### Define the variables

RamenPacks = model.addVar(vtype=GRB.INTEGER, name="RamenPacks")

FriesPacks = model.addVar(vtype=GRB.INTEGER, name="FriesPacks")



### Define the constraints

model.addConstr(CaloriesPerRamenPack * RamenPacks + CaloriesPerFriesPack * FriesPacks >= MinCalories)
model.addConstr(
    ProteinPerRamenPack * RamenPacks + ProteinPerFriesPack * FriesPacks >= MinProtein
)
model.addConstr(RamenPacks <= MaxRamenMealRatio * (RamenPacks + FriesPacks))
model.addConstr(RamenPacks >= 0)
model.addConstr(FriesPacks >= 0)


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
