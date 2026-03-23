
import os
import numpy as np
import json 
from gurobipy import Model, GRB, quicksum


model = Model("OptimizationProblem")

with open("data.json", "r") as f:
    data = json.load(f)




### Define the parameters

CamelCaravanCapacity = data["CamelCaravanCapacity"] # shape: [], definition: Amount of goods delivered per trip by a camel caravan

CamelCaravanTime = data["CamelCaravanTime"] # shape: [], definition: Time taken for one trip by a camel caravan

DesertTruckCapacity = data["DesertTruckCapacity"] # shape: [], definition: Amount of goods delivered per trip by a desert truck

DesertTruckTime = data["DesertTruckTime"] # shape: [], definition: Time taken for one trip by a desert truck

TotalGoodsToDeliver = data["TotalGoodsToDeliver"] # shape: [], definition: Total amount of goods to be delivered



### Define the variables

numCamelCaravans = model.addVar(vtype=GRB.INTEGER, name="numCamelCaravans")

numDesertTrucks = model.addVar(vtype=GRB.INTEGER, name="numDesertTrucks")



### Define the constraints

model.addConstr(CamelCaravanCapacity * numCamelCaravans + DesertTruckCapacity * numDesertTrucks >= TotalGoodsToDeliver)
model.addConstr(numCamelCaravans >= 0)
model.addConstr(numDesertTrucks >= 0)


### Define the objective

model.setObjective(
    CamelCaravanTime * numCamelCaravans + DesertTruckTime * numDesertTrucks,
    GRB.MINIMIZE
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
