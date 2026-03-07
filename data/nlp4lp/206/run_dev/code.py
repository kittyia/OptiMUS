
import os
import numpy as np
import json 
from gurobipy import Model, GRB, quicksum


model = Model("OptimizationProblem")

with open("data.json", "r") as f:
    data = json.load(f)




### Define the parameters

BatterAvailable = data["BatterAvailable"] # shape: [], definition: Total amount of batter available (in grams)

MilkAvailable = data["MilkAvailable"] # shape: [], definition: Total amount of milk available (in grams)

NumProducts = data["NumProducts"] # shape: [], definition: Number of different products

BatterPerProduct = data["BatterPerProduct"] # shape: ['NumProducts'], definition: Amount of batter required to produce one unit of each product

MilkPerProduct = data["MilkPerProduct"] # shape: ['NumProducts'], definition: Amount of milk required to produce one unit of each product

ProfitPerProduct = data["ProfitPerProduct"] # shape: ['NumProducts'], definition: Profit per unit of each product



### Define the variables

NumProduced = model.addVars(NumProducts, vtype=GRB.INTEGER, name="NumProduced")



### Define the constraints

model.addConstr(
    sum(BatterPerProduct[i] * NumProduced[i] for i in range(NumProducts)) 
    <= BatterAvailable
)
model.addConstr(
    sum(MilkPerProduct[i] * NumProduced[i] for i in range(NumProducts)) 
    <= MilkAvailable
)
for i in range(NumProducts):
    model.addConstr(NumProduced[i] >= 0)


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
