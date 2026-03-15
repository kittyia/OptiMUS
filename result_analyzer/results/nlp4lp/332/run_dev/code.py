
import os
import numpy as np
import json 
from gurobipy import Model, GRB, quicksum


model = Model("OptimizationProblem")

with open("data.json", "r") as f:
    data = json.load(f)




### Define the parameters

Capacity = data["Capacity"] # shape: [], definition: Total capacity of a floppy disk

NumFiles = data["NumFiles"] # shape: [], definition: Number of files to save

Size = data["Size"] # shape: ['NumFiles'], definition: Size of each file j



### Define the variables

assign = model.addVars(NumFiles, NumFiles, vtype=GRB.BINARY, name="assign")

useDisk = model.addVars(NumFiles, vtype=GRB.BINARY, name="useDisk")

nDisks = model.addVar(vtype=GRB.INTEGER, name="nDisks")



### Define the constraints

for j in range(NumFiles):
    model.addConstr(
        sum(assign[j, k] for k in range(NumFiles)) == 1
    )
for k in range(NumFiles):
    model.addConstr(
        sum(Size[j] * assign[j, k] for j in range(NumFiles)) 
        <= Capacity * useDisk[k]
    )
model.addConstr(nDisks == sum(useDisk[k] for k in range(NumFiles)))
# The binary nature of assign[j,k] is enforced by defining the variable 
# with vtype=GRB.BINARY during variable creation, so no additional 
# constraints are required here.
for k in range(NumFiles):
    model.addConstr(useDisk[k] >= 0)
    model.addConstr(useDisk[k] <= 1)


### Define the objective

model.setObjective(quicksum(useDisk[k] for k in range(NumFiles)), GRB.MINIMIZE)


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
