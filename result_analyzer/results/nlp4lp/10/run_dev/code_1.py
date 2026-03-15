import os
import numpy as np
import json
from gurobipy import Model, GRB, quicksum


model = Model("OptimizationProblem")

with open("data.json", "r") as f:
    data = json.load(f)


### Define the parameters

NumItems = data["NumItems"]          # Number of different items
NumPackages = data["NumPackages"]    # Number of package types
Available = data["Available"]        # Available quantity of each item
Required = data["Required"]          # Required[i][j]: amount of item i in package j
PackageProfit = data["PackageProfit"]  # Profit per package


### Define the variables

PackagesProduced = model.addVars(
    NumPackages,
    vtype=GRB.INTEGER,
    lb=0,
    name="PackagesProduced"
)


### Define the constraints (one per item)

for i in range(NumItems):
    model.addConstr(
        quicksum(Required[i][p] * PackagesProduced[p] for p in range(NumPackages))
        <= Available[i],
        name=f"ItemConstraint_{i}"
    )


### Define the objective

model.setObjective(
    quicksum(PackageProfit[j] * PackagesProduced[j] for j in range(NumPackages)),
    GRB.MAXIMIZE
)


### Optimize the model

model.optimize()


### Output optimal objective value

if model.status == GRB.OPTIMAL:
    print("Optimal Objective Value:", model.objVal)
    with open("output_solution.txt", "w") as f:
        f.write(str(model.objVal))
else:
    with open("output_solution.txt", "w") as f:
        f.write(str(model.status))