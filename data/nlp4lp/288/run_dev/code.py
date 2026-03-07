
import os
import numpy as np
import json 
from gurobipy import Model, GRB, quicksum


model = Model("OptimizationProblem")

with open("data.json", "r") as f:
    data = json.load(f)




### Define the parameters

TotalHectares = data["TotalHectares"] # shape: [], definition: Total available hectares for farming

MinTomatoes = data["MinTomatoes"] # shape: [], definition: Minimum hectares of tomatoes to meet community demands

MinPotatoes = data["MinPotatoes"] # shape: [], definition: Minimum hectares of potatoes to meet community demands

MaxTomatoesToPotatoesRatio = data["MaxTomatoesToPotatoesRatio"] # shape: [], definition: Maximum ratio of tomato hectares to potato hectares

ProfitPerHectareTomatoes = data["ProfitPerHectareTomatoes"] # shape: [], definition: Profit per hectare of tomatoes

ProfitPerHectarePotatoes = data["ProfitPerHectarePotatoes"] # shape: [], definition: Profit per hectare of potatoes



### Define the variables

TomatoHectares = model.addVar(vtype=GRB.CONTINUOUS, name="TomatoHectares")

PotatoHectares = model.addVar(vtype=GRB.CONTINUOUS, name="PotatoHectares")



### Define the constraints

model.addConstr(TomatoHectares + PotatoHectares <= TotalHectares)
model.addConstr(TomatoHectares <= MaxTomatoesToPotatoesRatio * PotatoHectares)
model.addConstr(TomatoHectares >= MinTomatoes)
model.addConstr(PotatoHectares >= MinPotatoes)


### Define the objective

del.setObjective(ProfitPerHectareTomatoes * TomatoHectares + ProfitPerHectarePotatoes * PotatoHectares, GRB.MAXIMIZE


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
