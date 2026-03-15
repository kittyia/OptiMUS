import os
import numpy as np
import json
from gurobipy import Model, GRB, quicksum


model = Model("OptimizationProblem")

with open("data.json", "r") as f:
    data = json.load(f)


### Define the parameters

VanCapacity = data["VanCapacity"]  # Number of pairs of shoes a van can transport
TruckCapacity = data["TruckCapacity"]  # Number of pairs of shoes a truck can transport
MinPairsToSupply = data["MinPairsToSupply"]  # Minimum number of pairs of shoes to supply


### Define the variables

Vans = model.addVar(vtype=GRB.INTEGER, lb=0, name="Vans")
Trucks = model.addVar(vtype=GRB.INTEGER, lb=0, name="Trucks")


### Define the constraints

model.addConstr(VanCapacity * Vans + TruckCapacity * Trucks >= MinPairsToSupply)
model.addConstr(Trucks <= Vans)


### Define the objective

model.setObjective(Vans, GRB.MINIMIZE)


### Optimize the model

model.optimize()


### Output optimal objective value

if model.status == GRB.OPTIMAL:
    print("Optimal Objective Value: ", model.objVal)
    with open("output_solution.txt", "w") as f:
        f.write(str(model.objVal))
else:
    with open("output_solution.txt", "w") as f:
        f.write(str(model.status))