
import os
import numpy as np
import json 
from gurobipy import Model, GRB, quicksum


model = Model("OptimizationProblem")

with open("data.json", "r") as f:
    data = json.load(f)




### Define the parameters

DoughLarge = data["DoughLarge"] # shape: [], definition: Units of dough required per large pizza

DoughMedium = data["DoughMedium"] # shape: [], definition: Units of dough required per medium pizza

ToppingsLarge = data["ToppingsLarge"] # shape: [], definition: Units of toppings required per large pizza

ToppingsMedium = data["ToppingsMedium"] # shape: [], definition: Units of toppings required per medium pizza

BakingTimeLarge = data["BakingTimeLarge"] # shape: [], definition: Baking time per large pizza in minutes

BakingTimeMedium = data["BakingTimeMedium"] # shape: [], definition: Baking time per medium pizza in minutes

MinDough = data["MinDough"] # shape: [], definition: Minimum units of dough required

MinToppings = data["MinToppings"] # shape: [], definition: Minimum units of toppings required

MinMediumPizzas = data["MinMediumPizzas"] # shape: [], definition: Minimum number of medium pizzas to be made

MinRatioLargeToMedium = data["MinRatioLargeToMedium"] # shape: [], definition: Minimum ratio of large pizzas to medium pizzas



### Define the variables

LargePizzas = model.addVar(vtype=GRB.INTEGER, name="LargePizzas")

MediumPizzas = model.addVar(vtype=GRB.INTEGER, name="MediumPizzas")



### Define the constraints

model.addConstr(DoughLarge * LargePizzas + DoughMedium * MediumPizzas >= MinDough)
model.addConstr(ToppingsLarge * LargePizzas + ToppingsMedium * MediumPizzas >= MinToppings)
model.addConstr(MediumPizzas >= MinMediumPizzas)
model.addConstr(LargePizzas >= MinRatioLargeToMedium * MediumPizzas)


### Define the objective

model.setObjective(BakingTimeLarge * LargePizzas + BakingTimeMedium * MediumPizzas, GRB.MINIMIZE)


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
