
import os
import numpy as np
import json 
from gurobipy import Model, GRB, quicksum


model = Model("OptimizationProblem")

with open("data.json", "r") as f:
    data = json.load(f)




### Define the parameters

K = data["K"] # shape: [], definition: Number of data points

Y = data["Y"] # shape: ['K'], definition: Observed values of the dependent variable

X = data["X"] # shape: ['K'], definition: Observed values of the independent variable



### Define the variables

d = model.addVars(K, vtype=GRB.CONTINUOUS, name="d")



### Define the constraints

for k in range(K):
    model.addConstr(Y[k] - (slope * X[k] + intercept) <= d[k])
for k in range(K):
    model.addConstr(slope * X[k] + intercept - Y[k] <= d[k])
for k in range(K):
    model.addConstr(d[k] >= 0)


### Define the objective

model.setObjective(quicksum(d[k] for k in range(K)), GRB.MINIMIZE)


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
