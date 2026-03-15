
import os
import numpy as np
import json 
from gurobipy import Model, GRB, quicksum


model = Model("OptimizationProblem")

with open("data.json", "r") as f:
    data = json.load(f)




### Define the parameters

CostPlushToy = data["CostPlushToy"] # shape: [], definition: Cost to the store for one plush toy

CostDoll = data["CostDoll"] # shape: [], definition: Cost to the store for one doll

InventoryBudget = data["InventoryBudget"] # shape: [], definition: Maximum total cost for inventory

ProfitPlushToy = data["ProfitPlushToy"] # shape: [], definition: Profit earned per plush toy sold

ProfitDoll = data["ProfitDoll"] # shape: [], definition: Profit earned per doll sold

MinPlushSold = data["MinPlushSold"] # shape: [], definition: Minimum number of plush toys sold each month

MaxPlushSold = data["MaxPlushSold"] # shape: [], definition: Maximum number of plush toys sold each month

MaxDollToPlushRatio = data["MaxDollToPlushRatio"] # shape: [], definition: Maximum ratio of number of dolls sold to number of plush toys sold



### Define the variables

PlushToys = model.addVar(vtype=GRB.INTEGER, name="PlushToys")

Dolls = model.addVar(vtype=GRB.INTEGER, name="Dolls")



### Define the constraints

model.addConstr(CostPlushToy * PlushToys + CostDoll * Dolls <= InventoryBudget)
model.addConstr(PlushToys >= MinPlushSold)
model.addConstr(PlushToys <= MaxPlushSold)
model.addConstr(Dolls <= MaxDollToPlushRatio * PlushToys)
model.addConstr(Dolls >= 0)


### Define the objective

model.setObjective(ProfitPlushToy * PlushToys + ProfitDoll * Dolls, GRB.MAXIMIZE)


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
