
import os
import numpy as np
import json 
from gurobipy import Model, GRB, quicksum


model = Model("OptimizationProblem")

with open("data.json", "r") as f:
    data = json.load(f)




### Define the parameters

large_roll_width = data["large_roll_width"] # shape: [], definition: large_roll_width

demands = data["demands"] # shape: ['N'], definition: demands

roll_width_options = data["roll_width_options"] # shape: ['N'], definition: roll_width_options

patterns = data["patterns"] # shape: ['N', 'M'], definition: patterns



### Define the variables

amount = model.addVars(N, vtype=GRB.INTEGER, name="amount")



### Define the constraints

for j in range(len(demands)):
    model.addConstr(
        sum(patterns[i][j] * amount[i] for i in range(len(patterns))) >= demands[j]
    )
for i in range(N):
    model.addConstr(amount[i] >= 0)


### Define the objective

model.setObjective(quicksum(amount[i] for i in range(N)), GRB.MINIMIZE)


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
