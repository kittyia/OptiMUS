
import os
import numpy as np
import json 
from gurobipy import Model, GRB, quicksum


model = Model("OptimizationProblem")

with open("data.json", "r") as f:
    data = json.load(f)




### Define the parameters

CostNoodles = data["CostNoodles"] # shape: [], definition: Cost per serving of noodles

CostProteinBars = data["CostProteinBars"] # shape: [], definition: Cost per serving of protein bars

CaloriesNoodles = data["CaloriesNoodles"] # shape: [], definition: Calories per serving of noodles

CaloriesProteinBars = data["CaloriesProteinBars"] # shape: [], definition: Calories per serving of protein bars

ProteinNoodles = data["ProteinNoodles"] # shape: [], definition: Protein per serving of noodles

ProteinProteinBars = data["ProteinProteinBars"] # shape: [], definition: Protein per serving of protein bars

MinCalories = data["MinCalories"] # shape: [], definition: Minimum required calories per day

MinProtein = data["MinProtein"] # shape: [], definition: Minimum required protein per day



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

print("Optimal Objective Value: ", model.objVal)


if model.status == GRB.OPTIMAL:
    with open("output_solution.txt", "w") as f:
        f.write(str(model.objVal))
    print("Optimal Objective Value: ", model.objVal)
else:
    with open("output_solution.txt", "w") as f:
        f.write(model.status)
