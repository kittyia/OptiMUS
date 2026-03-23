
import os
import numpy as np
import json 
from gurobipy import Model, GRB, quicksum


model = Model("OptimizationProblem")

with open("data.json", "r") as f:
    data = json.load(f)




### Define the parameters

NumItems = data["NumItems"] # shape: [], definition: Number of different items to be liquidated

NumPackages = data["NumPackages"] # shape: [], definition: Number of different package types

Available = data["Available"] # shape: ['NumItems'], definition: Available quantity of each item

Required = data["Required"] # shape: ['NumItems', 'NumPackages'], definition: Amount of each item required to prepare one unit of each package

PackageProfit = data["PackageProfit"] # shape: ['NumPackages'], definition: Profit for each package



### Define the variables

BananaHatersPackages = model.addVar(vtype=GRB.INTEGER, name="BananaHatersPackages")

ComboPackages = model.addVar(vtype=GRB.INTEGER, name="ComboPackages")



### Define the constraints

model.addConstr(6 * BananaHatersPackages + 5 * ComboPackages <= 10)
model.addConstr(BananaHatersPackages >= 0)
model.addConstr(ComboPackages >= 0)


### Define the objective

model.setObjective(
    PackageProfit[0] * BananaHatersPackages + 
    PackageProfit[1] * ComboPackages,
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
