
import os
import numpy as np
import json 
from gurobipy import Model, GRB, quicksum


model = Model("OptimizationProblem")

with open("data.json", "r") as f:
    data = json.load(f)




### Define the parameters

O = data["O"] # shape: [], definition: Number of options

P = data["P"] # shape: [], definition: Number of price points

L = data["L"] # shape: [], definition: Number of processes

Allocated = data["Allocated"] # shape: ['O'], definition: Allocated resources for each option

Price = data["Price"] # shape: ['P'], definition: Price at each price point

Input = data["Input"] # shape: ['L', 'O'], definition: Input resources required for each option in each process

Output = data["Output"] # shape: ['L', 'P'], definition: Output produced for each price point in each process

Cost = data["Cost"] # shape: ['L'], definition: Cost for each process



### Define the variables

execute = model.addVars(L, vtype=GRB.CONTINUOUS, name="execute")



### Define the constraints

for i in range(O):
    model.addConstr(
        sum(Input[l][i] * execute[l] for l in range(L)) <= Allocated[i]
    )
for l in range(L):
    model.addConstr(execute[l] >= 0)


### Define the objective

model.setObjective(
    quicksum(
        (
            quicksum(Price[p] * Output[l][p] for p in range(P))
            - Cost[l] * quicksum(Output[l][p] for p in range(P))
        ) * execute[l]
        for l in range(L)
    ),
    GRB.MAXIMIZE
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
