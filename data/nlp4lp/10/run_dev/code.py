
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

PackagesProduced = model.addVars(NumPackages, vtype=GRB.INTEGER, name="PackagesProduced")



### Define the constraints

model.addConstr(
    sum(Required[0][p] * PackagesProduced[p] for p in range(NumPackages)) 
    <= Available[0]
)
model.addConstr(
    sum(Required[banana_index][p] * PackagesProduced[p] for p in range(NumPackages))
    <= Available[banana_index]
)
model.addConstr(
    sum(Required[grapes_index][p] * PackagesProduced[p] for p in range(NumPackages))
    <= Available[grapes_index]
)
model.addConstr(PackagesProduced[1] >= 0)
model.addConstr(PackagesProduced[1] >= 0)


### Define the objective

model.setObjective(
    quicksum(PackageProfit[j] * PackagesProduced[j] for j in range(NumPackages)),
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
