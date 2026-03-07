
import os
import numpy as np
import json 
from gurobipy import Model, GRB, quicksum


model = Model("OptimizationProblem")

with open("data.json", "r") as f:
    data = json.load(f)




### Define the parameters

NumProducts = data["NumProducts"] # shape: [], definition: Number of different products produced

NumResources = data["NumResources"] # shape: [], definition: Number of different resources used

Profit = data["Profit"] # shape: ['NumProducts'], definition: Profit per unit of each product

ResourceRequirement = data["ResourceRequirement"] # shape: ['NumResources', 'NumProducts'], definition: Amount of each resource required to produce one unit of each product

ResourceAvailability = data["ResourceAvailability"] # shape: ['NumResources'], definition: Amount of each resource available per week



### Define the variables

Elephants = model.addVar(vtype=GRB.INTEGER, name="Elephants")

Tigers = model.addVar(vtype=GRB.INTEGER, name="Tigers")



### Define the constraints

model.addConstr(50 * Elephants + 40 * Tigers <= 5000)
model.addConstr(20 * Elephants + 30 * Tigers <= 4000)
model.addConstr(Elephants >= 0)
model.addConstr(Tigers >= 0)


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
