
import os
import numpy as np
import json 
from gurobipy import Model, GRB, quicksum


model = Model("OptimizationProblem")

with open("data.json", "r") as f:
    data = json.load(f)




### Define the parameters

NumProducts = data["NumProducts"] # shape: [], definition: Number of products

NumMachines = data["NumMachines"] # shape: [], definition: Number of machines

ProfitPerBatch = data["ProfitPerBatch"] # shape: ['NumProducts'], definition: Profit per batch of each product

TimeRequired = data["TimeRequired"] # shape: ['NumMachines', 'NumProducts'], definition: Time required on each machine to produce one batch of each product

MaxHours = data["MaxHours"] # shape: ['NumMachines'], definition: Maximum available hours per year for each machine



### Define the variables

ProduceBatches = model.addVars(NumProducts, vtype=GRB.CONTINUOUS, name="ProduceBatches")



### Define the constraints

model.addConstr(TimeRequired[0][0] * ProduceBatches[0] + TimeRequired[0][1] * ProduceBatches[1] <= MaxHours[0])
model.addConstr(2.5 * ProduceBatches[1] + 3.5 * ProduceBatches[2] <= 4000)
for p in range(NumProducts):
    model.addConstr(ProduceBatches[p] >= 0)


### Define the objective

model.setObjective(quicksum(ProfitPerBatch[i] * ProduceBatches[i] for i in range(NumProducts)), GRB.MAXIMIZE)


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
