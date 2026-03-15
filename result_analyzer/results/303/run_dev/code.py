
import os
import numpy as np
import json 
from gurobipy import Model, GRB, quicksum


model = Model("OptimizationProblem")

with open("data.json", "r") as f:
    data = json.load(f)




### Define the parameters

P = data["P"] # shape: [], definition: Number of products

Cash = data["Cash"] # shape: [], definition: Initial cash available for investment

Hour = data["Hour"] # shape: ['P'], definition: Hours required to produce one unit of product i

Cost = data["Cost"] # shape: ['P'], definition: Cost to produce one unit of product i

Price = data["Price"] # shape: ['P'], definition: Selling price for one unit of product i

InvestPercentage = data["InvestPercentage"] # shape: ['P'], definition: Percentage of income to reinvest for product i

UpgradeHours = data["UpgradeHours"] # shape: [], definition: Hours required for upgrading the machinery

UpgradeCost = data["UpgradeCost"] # shape: [], definition: Cost associated with upgrading the machinery

AvailableHours = data["AvailableHours"] # shape: [], definition: Total available machine hours



### Define the variables

production = model.addVars(P, vtype=GRB.CONTINUOUS, name="production")

upgrade = model.addVar(vtype=GRB.BINARY, name="upgrade")



### Define the constraints

for i in range(P):
    model.addConstr(production[i] >= 0)
model.addConstr(upgrade >= 0)
model.addConstr(upgrade <= 1)
model.addConstr(
    sum(Hour[i] * production[i] for i in range(P)) 
    <= AvailableHours + UpgradeHours * upgrade
)
model.addConstr(
    sum(Cost[i] * production[i] for i in range(P)) + UpgradeCost * upgrade
    <= Cash + sum(InvestPercentage[i] * Price[i] * production[i] for i in range(P))
)


### Define the objective

model.setObjective(
    quicksum(
        (Price[i] - Cost[i] - InvestPercentage[i] * Price[i]) * production[i]
        for i in range(P)
    ) - UpgradeCost * upgrade,
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
