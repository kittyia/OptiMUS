
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

vans = model.addVar(vtype=GRB.INTEGER, name="vans")

trucks = model.addVar(vtype=GRB.INTEGER, name="trucks")



### Define the constraints

model.addConstr(VanCapacity * vans + TruckCapacity * trucks >= MinPairsToSupply)
model.addConstr(trucks <= vans)
model.addConstr(vans >= 0)
model.addConstr(trucks >= 0)


### Define the objective

model.setObjective(vans, GRB.MINIMIZE)


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
