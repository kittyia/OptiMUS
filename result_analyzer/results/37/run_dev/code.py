
import os
import numpy as np
import json 
from gurobipy import Model, GRB, quicksum


model = Model("OptimizationProblem")

with open("data.json", "r") as f:
    data = json.load(f)




### Define the parameters

NumProducts = data["NumProducts"] # shape: [], definition: Number of products baked

NumResources = data["NumResources"] # shape: [], definition: Number of resource types

Profit = data["Profit"] # shape: ['NumProducts'], definition: Profit per batch of each product

ResourceTime = data["ResourceTime"] # shape: ['NumResources', 'NumProducts'], definition: Time required per batch of each product for each resource

ResourceAvailability = data["ResourceAvailability"] # shape: ['NumResources'], definition: Total available time per resource



### Define the variables

Batches = model.addVars(NumProducts, vtype=GRB.CONTINUOUS, name="Batches")



### Define the constraints

model.addConstr(2 * Batches[0] + 1 * Batches[1] <= 70)
model.addConstr(0.25 * Batches[0] + 2 * Batches[1] <= 32)
model.addConstr(Batches[1] >= 0)
model.addConstr(Batches[1] >= 0)


### Define the objective

model.setObjective(quicksum(Profit[i] * Batches[i] for i in range(NumProducts)), GRB.MAXIMIZE)


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
