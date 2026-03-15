
import os
import numpy as np
import json 
from gurobipy import Model, GRB, quicksum


model = Model("OptimizationProblem")

with open("data.json", "r") as f:
    data = json.load(f)




### Define the parameters

NumProducts = data["NumProducts"] # shape: [], definition: Number of different products

NumMachines = data["NumMachines"] # shape: [], definition: Number of different machines

ProduceTime = data["ProduceTime"] # shape: ['NumProducts', 'NumMachines'], definition: Time to produce one unit of product k on machine m

AvailableTime = data["AvailableTime"] # shape: ['NumMachines'], definition: Total available time on machine m

Profit = data["Profit"] # shape: ['NumProducts'], definition: Profit from producing one unit of product k



### Define the variables

quantity = model.addVars(NumProducts, vtype=GRB.CONTINUOUS, name="quantity")



### Define the constraints

for m in range(NumMachines):
    model.addConstr(
        sum(ProduceTime[k][m] * quantity[k] for k in range(NumProducts)) 
        <= AvailableTime[m]
    )
for k in range(NumProducts):
    model.addConstr(quantity[k] >= 0)


### Define the objective

model.setObjective(quicksum(Profit[k] * quantity[k] for k in range(NumProducts)), GRB.MAXIMIZE)


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
