
import os
import numpy as np
import json 
from gurobipy import Model, GRB, quicksum


model = Model("OptimizationProblem")

with open("data.json", "r") as f:
    data = json.load(f)




### Define the parameters

ProfitRegular = data["ProfitRegular"] # shape: [], definition: Profit per regular model

ProfitPremium = data["ProfitPremium"] # shape: [], definition: Profit per premium model

DemandRegular = data["DemandRegular"] # shape: [], definition: Daily demand for regular models

DemandPremium = data["DemandPremium"] # shape: [], definition: Daily demand for premium models

MaxCarsTotal = data["MaxCarsTotal"] # shape: [], definition: Maximum number of cars that can be made per day



### Define the variables

x1 = model.addVar(vtype=GRB.CONTINUOUS, name="x1")

x2 = model.addVar(vtype=GRB.CONTINUOUS, name="x2")



### Define the constraints

model.addConstr(x1 >= 0)
model.addConstr(x2 >= 0)
model.addConstr(x1 <= DemandRegular)
model.addConstr(x2 <= DemandPremium)
model.addConstr(x1 + x2 <= MaxCarsTotal)


### Define the objective

model.setObjective(ProfitRegular * x1 + ProfitPremium * x2, GRB.MAXIMIZE)


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
