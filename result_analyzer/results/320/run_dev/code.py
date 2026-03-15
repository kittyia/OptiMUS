
import os
import numpy as np
import json 
from gurobipy import Model, GRB, quicksum


model = Model("OptimizationProblem")

with open("data.json", "r") as f:
    data = json.load(f)




### Define the parameters

NumObs = data["NumObs"] # shape: [], definition: Number of observed data points

Y = data["Y"] # shape: ['NumObs'], definition: Observed values of y

X = data["X"] # shape: ['NumObs'], definition: Observed values of x



### Define the variables

slope = model.addVar(vtype=GRB.CONTINUOUS, name="slope")

intercept = model.addVar(vtype=GRB.CONTINUOUS, name="intercept")

t = model.addVar(vtype=GRB.CONTINUOUS, name="t")



### Define the constraints

for k in range(NumObs):
    model.addConstr(Y[k] - (slope * X[k] + intercept) <= t)
for k in range(NumObs):
    model.addConstr(slope * X[k] + intercept - Y[k] <= t)


### Define the objective

model.setObjective(t, GRB.MINIMIZE)


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
