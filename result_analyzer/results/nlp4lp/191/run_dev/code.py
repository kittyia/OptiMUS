
import os
import numpy as np
import json 
from gurobipy import Model, GRB, quicksum


model = Model("OptimizationProblem")

with open("data.json", "r") as f:
    data = json.load(f)




### Define the parameters

NumProducts = data["NumProducts"] # shape: [], definition: Number of different products sold by the company

MoverTimePerProduct = data["MoverTimePerProduct"] # shape: ['NumProducts'], definition: Amount of mover time required to sell one unit of each product

SetupTimePerProduct = data["SetupTimePerProduct"] # shape: ['NumProducts'], definition: Amount of setup time required to sell one unit of each product

ProfitPerProduct = data["ProfitPerProduct"] # shape: ['NumProducts'], definition: Profit per unit of each product

TotalMoverTime = data["TotalMoverTime"] # shape: [], definition: Total available mover time

TotalSetupTime = data["TotalSetupTime"] # shape: [], definition: Total available setup time



### Define the variables

Quantity = model.addVars(NumProducts, vtype=GRB.INTEGER, name="Quantity")



### Define the constraints

model.addConstr(
    sum(MoverTimePerProduct[i] * Quantity[i] for i in range(NumProducts))
    <= TotalMoverTime
)
model.addConstr(
    sum(SetupTimePerProduct[i] * Quantity[i] for i in range(NumProducts))
    <= TotalSetupTime
)
for i in range(NumProducts):
    model.addConstr(Quantity[i] >= 0)


### Define the objective

model.setObjective(quicksum(ProfitPerProduct[i] * Quantity[i] for i in range(NumProducts)), GRB.MAXIMIZE)


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
