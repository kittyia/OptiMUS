
import os
import numpy as np
import json 
from gurobipy import Model, GRB, quicksum


model = Model("OptimizationProblem")

with open("data.json", "r") as f:
    data = json.load(f)




### Define the parameters

VanCapacity = data["VanCapacity"] # shape: [], definition: Number of pairs of shoes a van can transport

TruckCapacity = data["TruckCapacity"] # shape: [], definition: Number of pairs of shoes a truck can transport

MinPairsToSupply = data["MinPairsToSupply"] # shape: [], definition: Minimum number of pairs of shoes to supply



### Define the variables

Vans = model.addVar(vtype=GRB.INTEGER, name="Vans")

Trucks = model.addVar(vtype=GRB.INTEGER, name="Trucks")



### Define the constraints

model.addConstr(VanCapacity * Vans + TruckCapacity * Trucks >= MinPairsToSupply)
model.addConstr(Trucks <= Vans)
model.addConstr(Trucks >= 0)
model.addConstr(Vans >= 0)
model.addConstr(Trucks >= 0)


### Define the objective

del.setObjective(Vans, GRB.MINIMIZE


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
