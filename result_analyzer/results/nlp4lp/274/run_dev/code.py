
import os
import numpy as np
import json 
from gurobipy import Model, GRB, quicksum


model = Model("OptimizationProblem")

with open("data.json", "r") as f:
    data = json.load(f)




### Define the parameters

T = data["T"] # shape: [], definition: Total number of days in the scheduling period

Period = data["Period"] # shape: [], definition: Number of consecutive days each nurse works

Demand = data["Demand"] # shape: ['T'], definition: Number of nurses required on each day



### Define the variables

Start = model.addVars(T, vtype=GRB.INTEGER, name="Start")



### Define the constraints

for t in range(T):
    model.addConstr(
        sum(Start[(t - k) % T] for k in range(Period)) >= Demand[t]
    )
for t in range(T):
    model.addConstr(Start[t] >= 0)


### Define the objective

model.setObjective(quicksum(Start[t] for t in range(T)), GRB.MINIMIZE)


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
