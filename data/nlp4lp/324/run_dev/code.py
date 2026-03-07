
import os
import numpy as np
import json 
from gurobipy import Model, GRB, quicksum


model = Model("OptimizationProblem")

with open("data.json", "r") as f:
    data = json.load(f)




### Define the parameters

C = data["C"] # shape: [], definition: Total Capacity of the Knapsack

Value = data["Value"] # shape: ['NumItems'], definition: Value of item k

Size = data["Size"] # shape: ['NumItems'], definition: Size of item k

NumItems = data["NumItems"] # shape: [], definition: Number of items



### Define the variables

isincluded = model.addVars(NumItems, vtype=GRB.BINARY, name="isincluded")



### Define the constraints

for k in range(NumItems):
    model.addConstr(isincluded[k] >= 0)
    model.addConstr(isincluded[k] <= 1)
model.addConstr(
    sum(Size[k] * isincluded[k] for k in range(NumItems)) <= C
)


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
