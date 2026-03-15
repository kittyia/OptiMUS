
import os
import numpy as np
import json 
from gurobipy import Model, GRB, quicksum


model = Model("OptimizationProblem")

with open("data.json", "r") as f:
    data = json.load(f)




### Define the parameters

CaloriesCheesecake = data["CaloriesCheesecake"] # shape: [], definition: Calories per slice of cheesecake

SugarCheesecake = data["SugarCheesecake"] # shape: [], definition: Sugar per slice of cheesecake

CaloriesCaramelCake = data["CaloriesCaramelCake"] # shape: [], definition: Calories per slice of caramel cake

SugarCaramelCake = data["SugarCaramelCake"] # shape: [], definition: Sugar per slice of caramel cake

MinCheesecakeToCaramelRatio = data["MinCheesecakeToCaramelRatio"] # shape: [], definition: Minimum ratio of cheesecake slices to caramel cake slices

MinCaramelSlices = data["MinCaramelSlices"] # shape: [], definition: Minimum number of caramel cake slices

MaxTotalCalories = data["MaxTotalCalories"] # shape: [], definition: Maximum total calories that can be consumed in one day



### Define the variables

CaramelSlices = model.addVar(vtype=GRB.INTEGER, name="CaramelSlices")

CheesecakeSlices = model.addVar(vtype=GRB.INTEGER, name="CheesecakeSlices")



### Define the constraints

model.addConstr(CaramelSlices >= MinCaramelSlices)
model.addConstr(CheesecakeSlices >= MinCheesecakeToCaramelRatio * CaramelSlices)
model.addConstr(CaloriesCheesecake * CheesecakeSlices + CaloriesCaramelCake * CaramelSlices <= MaxTotalCalories)


### Define the objective

model.setObjective(
    SugarCheesecake * CheesecakeSlices + 
    SugarCaramelCake * CaramelSlices,
    GRB.MAXIMIZE
)


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
