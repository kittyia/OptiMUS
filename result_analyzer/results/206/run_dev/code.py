
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

crepeCakes = model.addVar(vtype=GRB.INTEGER, name="crepeCakes")

spongeCakes = model.addVar(vtype=GRB.INTEGER, name="spongeCakes")

birthdayCakes = model.addVar(vtype=GRB.INTEGER, name="birthdayCakes")



### Define the constraints

model.addConstr(400 * crepeCakes + 500 * spongeCakes + 450 * birthdayCakes <= 20000)
model.addConstr(200 * crepeCakes + 300 * spongeCakes + 350 * birthdayCakes <= 14000)
model.addConstr(crepeCakes >= 0)
model.addConstr(spongeCakes >= 0)
model.addConstr(birthdayCakes >= 0)
model.addConstr(crepeCakes >= 0)
model.addConstr(spongeCakes >= 0)
model.addConstr(birthdayCakes >= 0)


### Define the objective

model.setObjective(12 * crepeCakes + 10 * spongeCakes + 15 * birthdayCakes, GRB.MAXIMIZE)


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
