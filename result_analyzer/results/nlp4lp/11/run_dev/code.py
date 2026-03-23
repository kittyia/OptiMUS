
import os
import numpy as np
import json 
from gurobipy import Model, GRB, quicksum


model = Model("OptimizationProblem")

with open("data.json", "r") as f:
    data = json.load(f)




### Define the parameters

MixerMaximumHours = data["MixerMaximumHours"] # shape: [], definition: Maximum available operating hours per year for the stand mixer

OvenMaximumHours = data["OvenMaximumHours"] # shape: [], definition: Maximum available operating hours per year for the oven

BreadMixerTime = data["BreadMixerTime"] # shape: [], definition: Number of hours the stand mixer is required to bake one loaf of bread

BreadOvenTime = data["BreadOvenTime"] # shape: [], definition: Number of hours the oven is required to bake one loaf of bread

CookiesMixerTime = data["CookiesMixerTime"] # shape: [], definition: Number of hours the stand mixer is required to bake one batch of cookies

CookiesOvenTime = data["CookiesOvenTime"] # shape: [], definition: Number of hours the oven is required to bake one batch of cookies

BreadProfit = data["BreadProfit"] # shape: [], definition: Profit earned per loaf of bread

CookiesProfit = data["CookiesProfit"] # shape: [], definition: Profit earned per batch of cookies



### Define the variables

BreadQuantity = model.addVar(vtype=GRB.CONTINUOUS, name="BreadQuantity")

CookiesQuantity = model.addVar(vtype=GRB.CONTINUOUS, name="CookiesQuantity")



### Define the constraints

model.addConstr(3 * BreadQuantity + 1 * CookiesQuantity <= OvenMaximumHours)
model.addConstr(BreadQuantity >= 0)
model.addConstr(CookiesQuantity >= 0)


### Define the objective

model.setObjective(BreadProfit * BreadQuantity + CookiesProfit * CookiesQuantity, GRB.MAXIMIZE)


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
