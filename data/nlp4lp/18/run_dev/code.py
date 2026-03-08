
import os
import numpy as np
import json 
from gurobipy import Model, GRB, quicksum


model = Model("OptimizationProblem")

with open("data.json", "r") as f:
    data = json.load(f)




### Define the parameters

ProfitPhone = data["ProfitPhone"] # shape: [], definition: Profit earned per phone

ProfitLaptop = data["ProfitLaptop"] # shape: [], definition: Profit earned per laptop

SpacePhone = data["SpacePhone"] # shape: [], definition: Floor space required per phone (sq ft)

SpaceLaptop = data["SpaceLaptop"] # shape: [], definition: Floor space required per laptop (sq ft)

TotalSpace = data["TotalSpace"] # shape: [], definition: Total available floor space (sq ft)

MinLaptopPercentage = data["MinLaptopPercentage"] # shape: [], definition: Minimum percentage of laptops required in inventory

CostPhone = data["CostPhone"] # shape: [], definition: Cost per phone

CostLaptop = data["CostLaptop"] # shape: [], definition: Cost per laptop

MaxBudget = data["MaxBudget"] # shape: [], definition: Maximum total budget



### Define the variables

Phones = model.addVar(vtype=GRB.INTEGER, name="Phones")

Laptops = model.addVar(vtype=GRB.INTEGER, name="Laptops")



### Define the constraints

model.addConstr(CostPhone * Phones + CostLaptop * Laptops <= MaxBudget)
model.addConstr(Laptops >= MinLaptopPercentage * (Phones + Laptops))
model.addConstr(Phones >= 0)


### Define the objective

model.setObjective(ProfitPhone * Phones + ProfitLaptop * Laptops, GRB.MAXIMIZE)


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
