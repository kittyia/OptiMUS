
import os
import numpy as np
import json 
from gurobipy import Model, GRB, quicksum


model = Model("OptimizationProblem")

with open("data.json", "r") as f:
    data = json.load(f)




### Define the parameters

SteelQuantity = data["SteelQuantity"] # shape: [], definition: Amount of steel to produce in tons

ManganesePercent = data["ManganesePercent"] # shape: [], definition: Percentage of manganese in the steel required

SiliconMinPercent = data["SiliconMinPercent"] # shape: [], definition: Minimum percentage of silicon in the steel required

SiliconMaxPercent = data["SiliconMaxPercent"] # shape: [], definition: Maximum percentage of silicon in the steel allowed

NumMinerals = data["NumMinerals"] # shape: [], definition: Number of different types of minerals available

SiliconContent = data["SiliconContent"] # shape: ['NumMinerals'], definition: Silicon content in the k-th stock

ManganeseContent = data["ManganeseContent"] # shape: ['NumMinerals'], definition: Manganese content in the k-th stock

ManganesePrice = data["ManganesePrice"] # shape: [], definition: Price of manganese per ton

MaterialCost = data["MaterialCost"] # shape: ['NumMinerals'], definition: Cost of the k-th stock material per ton

SellingPrice = data["SellingPrice"] # shape: [], definition: Selling price of steel per ton

MeltingPrice = data["MeltingPrice"] # shape: [], definition: Price to melt one ton of steel



### Define the variables

amount = model.addVars(NumMinerals, vtype=GRB.CONTINUOUS, name="amount")

numMang = model.addVar(vtype=GRB.CONTINUOUS, name="numMang")



### Define the constraints

model.addConstr(
    sum(amount[k] for k in range(NumMinerals)) + numMang == SteelQuantity
)
model.addConstr(
    sum(ManganeseContent[k] * amount[k] for k in range(NumMinerals)) + numMang
    >= ManganesePercent * SteelQuantity
)
model.addConstr(
    sum((SiliconContent[k] / 100.0) * amount[k] for k in range(NumMinerals)) 
    >= (SiliconMinPercent / 100.0) * SteelQuantity
)

model.addConstr(
    sum((SiliconContent[k] / 100.0) * amount[k] for k in range(NumMinerals)) 
    <= (SiliconMaxPercent / 100.0) * SteelQuantity
)
for k in range(NumMinerals):
    model.addConstr(amount[k] >= 0)

model.addConstr(numMang >= 0)


### Define the objective

model.setObjective(
    SellingPrice * SteelQuantity
    - quicksum(MaterialCost[k] * amount[k] for k in range(NumMinerals))
    - ManganesePrice * numMang
    - MeltingPrice * quicksum(amount[k] for k in range(NumMinerals)),
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
