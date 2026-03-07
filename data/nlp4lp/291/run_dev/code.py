
import os
import numpy as np
import json 
from gurobipy import Model, GRB, quicksum


model = Model("OptimizationProblem")

with open("data.json", "r") as f:
    data = json.load(f)




### Define the parameters

MaxExpenditure = data["MaxExpenditure"] # shape: [], definition: Maximum monthly expenditure on carrots and cucumbers

CostCarrot = data["CostCarrot"] # shape: [], definition: Cost of one carrot

CostCucumber = data["CostCucumber"] # shape: [], definition: Cost of one cucumber

ProfitCarrot = data["ProfitCarrot"] # shape: [], definition: Profit from selling one carrot

ProfitCucumber = data["ProfitCucumber"] # shape: [], definition: Profit from selling one cucumber

CucumberFraction = data["CucumberFraction"] # shape: [], definition: Maximum ratio of cucumbers sold to carrots sold

MinCarrots = data["MinCarrots"] # shape: [], definition: Minimum number of carrots sold per month

MaxCarrots = data["MaxCarrots"] # shape: [], definition: Maximum number of carrots sold per month



### Define the variables

CarrotsSold = model.addVar(vtype=GRB.INTEGER, name="CarrotsSold")

CucumbersSold = model.addVar(vtype=GRB.INTEGER, name="CucumbersSold")



### Define the constraints

model.addConstr(CostCarrot * CarrotsSold + CostCucumber * CucumbersSold <= MaxExpenditure)
model.addConstr(CucumbersSold <= CucumberFraction * CarrotsSold)
model.addConstr(CarrotsSold >= MinCarrots)
model.addConstr(CarrotsSold <= MaxCarrots)
model.addConstr(CucumbersSold >= 0)


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
