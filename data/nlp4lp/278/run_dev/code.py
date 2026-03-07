
import os
import numpy as np
import json 
from gurobipy import Model, GRB, quicksum


model = Model("OptimizationProblem")

with open("data.json", "r") as f:
    data = json.load(f)




### Define the parameters

NumParts = data["NumParts"] # shape: [], definition: Number of types of spare parts

NumMachines = data["NumMachines"] # shape: [], definition: Number of machines

Time = data["Time"] # shape: ['NumParts', 'NumMachines'], definition: Worker-hours required to produce one unit of part k on machine s

Profit = data["Profit"] # shape: ['NumParts'], definition: Profit from producing one unit of part k

Capacity = data["Capacity"] # shape: ['NumMachines'], definition: Available worker-hours capacity of machine s



### Define the variables

x = model.addVars(NumParts, vtype=GRB.CONTINUOUS, name="x")



### Define the constraints

for s in range(NumMachines):
    model.addConstr(
        sum(Time[k][s] * x[k] for k in range(NumParts)) <= Capacity[s]
    )
for k in range(NumParts):
    model.addConstr(x[k] >= 0)


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
