import os
import numpy as np
import json 
from gurobipy import Model, GRB, quicksum


model = Model("OptimizationProblem")

with open("data.json", "r") as f:
    data = json.load(f)


### Define the parameters

CostNoodles = data["CostNoodles"]  # Cost per serving of noodles
CostProteinBars = data["CostProteinBars"]  # Cost per serving of protein bars
CaloriesNoodles = data["CaloriesNoodles"]  # Calories per serving of noodles
CaloriesProteinBars = data["CaloriesProteinBars"]  # Calories per serving of protein bars
ProteinNoodles = data["ProteinNoodles"]  # Protein per serving of noodles
ProteinProteinBars = data["ProteinProteinBars"]  # Protein per serving of protein bars
MinCalories = data["MinCalories"]  # Minimum required calories per day
MinProtein = data["MinProtein"]  # Minimum required protein per day


### Define the variables

ServingsNoodles = model.addVar(vtype=GRB.CONTINUOUS, name="ServingsNoodles")
ServingsProteinBars = model.addVar(vtype=GRB.CONTINUOUS, name="ServingsProteinBars")


### Define the constraints

model.addConstr(CaloriesNoodles * ServingsNoodles + CaloriesProteinBars * ServingsProteinBars >= MinCalories)
model.addConstr(ProteinNoodles * ServingsNoodles + ProteinProteinBars * ServingsProteinBars >= MinProtein)
model.addConstr(ServingsNoodles >= 0)
model.addConstr(ServingsProteinBars >= 0)


### Define the objective

model.setObjective(CostNoodles * ServingsNoodles + CostProteinBars * ServingsProteinBars, GRB.MINIMIZE)


### Optimize the model

model.optimize()


### Output optimal objective value

if model.status == GRB.OPTIMAL:
    print("Optimal Objective Value: ", model.objVal)
    with open("output_solution.txt", "w") as f:
        f.write(str(model.objVal))
else:
    with open("output_solution.txt", "w") as f:
        f.write(str(model.status))