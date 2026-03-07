
import os
import numpy as np
import json 
from gurobipy import Model, GRB, quicksum


model = Model("OptimizationProblem")

with open("data.json", "r") as f:
    data = json.load(f)




### Define the parameters

NumProducts = data["NumProducts"] # shape: [], definition: Number of different products manufactured

NumMachines = data["NumMachines"] # shape: [], definition: Number of different machine types

TimeRequired = data["TimeRequired"] # shape: ['NumMachines', 'NumProducts'], definition: Time required by each machine to produce each product

AvailableTime = data["AvailableTime"] # shape: ['NumMachines'], definition: Available time per machine per day

ProfitPerProduct = data["ProfitPerProduct"] # shape: ['NumProducts'], definition: Profit per product



### Define the variables

GraphReams = model.addVar(vtype=GRB.CONTINUOUS, name="GraphReams")

MusicReams = model.addVar(vtype=GRB.CONTINUOUS, name="MusicReams")



### Define the constraints

model.addConstr(3 * GraphReams + 1.5 * MusicReams <= 350)
model.addConstr(5.5 * GraphReams + 3 * MusicReams <= 350)
model.addConstr(GraphReams >= 0)
model.addConstr(MusicReams >= 0)


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
