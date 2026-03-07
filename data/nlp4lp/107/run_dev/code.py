
import os
import numpy as np
import json 
from gurobipy import Model, GRB, quicksum


model = Model("OptimizationProblem")

with open("data.json", "r") as f:
    data = json.load(f)




### Define the parameters

FatPerBurger = data["FatPerBurger"] # shape: [], definition: Units of fat per burger

FatPerPizzaSlice = data["FatPerPizzaSlice"] # shape: [], definition: Units of fat per slice of pizza

CaloriesPerBurger = data["CaloriesPerBurger"] # shape: [], definition: Calories per burger

CaloriesPerPizzaSlice = data["CaloriesPerPizzaSlice"] # shape: [], definition: Calories per slice of pizza

CholesterolPerBurger = data["CholesterolPerBurger"] # shape: [], definition: Units of cholesterol per burger

CholesterolPerPizzaSlice = data["CholesterolPerPizzaSlice"] # shape: [], definition: Units of cholesterol per slice of pizza

MinFat = data["MinFat"] # shape: [], definition: Minimum total units of fat required

MinCalories = data["MinCalories"] # shape: [], definition: Minimum total calories required

MinPizzaToBurgerRatio = data["MinPizzaToBurgerRatio"] # shape: [], definition: Minimum ratio of slices of pizza to burgers



### Define the variables

Burgers = model.addVar(vtype=GRB.INTEGER, name="Burgers")

PizzaSlices = model.addVar(vtype=GRB.INTEGER, name="PizzaSlices")



### Define the constraints

model.addConstr(FatPerBurger * Burgers + FatPerPizzaSlice * PizzaSlices >= MinFat)
model.addConstr(PizzaSlices >= 2 * Burgers)
model.addConstr(Burgers >= 0)
model.addConstr(PizzaSlices >= 0)


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
