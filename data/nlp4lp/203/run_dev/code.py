
import os
import numpy as np
import json 
from gurobipy import Model, GRB, quicksum


model = Model("OptimizationProblem")

with open("data.json", "r") as f:
    data = json.load(f)




### Define the parameters

RegularHandbagProfit = data["RegularHandbagProfit"] # shape: [], definition: Profit per regular handbag

PremiumHandbagProfit = data["PremiumHandbagProfit"] # shape: [], definition: Profit per premium handbag

RegularHandbagCost = data["RegularHandbagCost"] # shape: [], definition: Manufacturing cost per regular handbag

PremiumHandbagCost = data["PremiumHandbagCost"] # shape: [], definition: Manufacturing cost per premium handbag

TotalBudget = data["TotalBudget"] # shape: [], definition: Total budget available for manufacturing

MaxHandbagsPerMonth = data["MaxHandbagsPerMonth"] # shape: [], definition: Maximum number of handbags that can be sold per month



### Define the variables

RegularHandbags = model.addVar(vtype=GRB.INTEGER, name="RegularHandbags")

PremiumHandbags = model.addVar(vtype=GRB.INTEGER, name="PremiumHandbags")



### Define the constraints

model.addConstr(RegularHandbagCost * RegularHandbags + PremiumHandbagCost * PremiumHandbags <= TotalBudget)
model.addConstr(RegularHandbags + PremiumHandbags <= MaxHandbagsPerMonth)
model.addConstr(RegularHandbags >= 0)
model.addConstr(PremiumHandbags >= 0)


### Define the objective




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
