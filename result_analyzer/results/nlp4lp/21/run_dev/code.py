
import os
import numpy as np
import json 
from gurobipy import Model, GRB, quicksum


model = Model("OptimizationProblem")

with open("data.json", "r") as f:
    data = json.load(f)




### Define the parameters

ManufacturingCostPremiumDesktop = data["ManufacturingCostPremiumDesktop"] # shape: [], definition: Manufacturing cost of a premium desktop

ManufacturingCostRegularDesktop = data["ManufacturingCostRegularDesktop"] # shape: [], definition: Manufacturing cost of a regular desktop

ProfitPremiumDesktop = data["ProfitPremiumDesktop"] # shape: [], definition: Profit from a premium desktop

ProfitRegularDesktop = data["ProfitRegularDesktop"] # shape: [], definition: Profit from a regular desktop

MaxDesktopSales = data["MaxDesktopSales"] # shape: [], definition: Maximum number of desktops sold per month

MaxManufacturingBudget = data["MaxManufacturingBudget"] # shape: [], definition: Maximum spending on making the desktops



### Define the variables

PremiumDesktops = model.addVar(vtype=GRB.INTEGER, name="PremiumDesktops")

RegularDesktops = model.addVar(vtype=GRB.INTEGER, name="RegularDesktops")



### Define the constraints

model.addConstr(PremiumDesktops + RegularDesktops <= MaxDesktopSales)
model.addConstr(
    ManufacturingCostPremiumDesktop * PremiumDesktops
    + ManufacturingCostRegularDesktop * RegularDesktops
    <= MaxManufacturingBudget
)
model.addConstr(PremiumDesktops >= 0)
model.addConstr(RegularDesktops >= 0)


### Define the objective

model.setObjective(
    ProfitPremiumDesktop * PremiumDesktops +
    ProfitRegularDesktop * RegularDesktops,
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
