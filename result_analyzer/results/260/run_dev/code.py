
import os
import numpy as np
import json 
from gurobipy import Model, GRB, quicksum


model = Model("OptimizationProblem")

with open("data.json", "r") as f:
    data = json.load(f)




### Define the parameters

ProteinPerSmoothie = data["ProteinPerSmoothie"] # shape: [], definition: Amount of protein per smoothie

CaloriesPerSmoothie = data["CaloriesPerSmoothie"] # shape: [], definition: Amount of calories per smoothie

ProteinPerBar = data["ProteinPerBar"] # shape: [], definition: Amount of protein per protein bar

CaloriesPerBar = data["CaloriesPerBar"] # shape: [], definition: Amount of calories per protein bar

BarToSmoothieRatio = data["BarToSmoothieRatio"] # shape: [], definition: Ratio of protein bars to smoothies

MaxCalories = data["MaxCalories"] # shape: [], definition: Maximum allowable total calories



### Define the variables

Smoothies = model.addVar(vtype=GRB.INTEGER, name="Smoothies")

ProteinBars = model.addVar(vtype=GRB.INTEGER, name="ProteinBars")



### Define the constraints

model.addConstr(ProteinBars == BarToSmoothieRatio * Smoothies)
model.addConstr(CaloriesPerSmoothie * Smoothies + CaloriesPerBar * ProteinBars <= MaxCalories)
model.addConstr(Smoothies >= 0)


### Define the objective

model.setObjective(ProteinPerSmoothie * Smoothies + ProteinPerBar * ProteinBars, GRB.MAXIMIZE)


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
