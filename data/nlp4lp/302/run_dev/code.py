
import os
import numpy as np
import json 
from gurobipy import Model, GRB, quicksum


model = Model("OptimizationProblem")

with open("data.json", "r") as f:
    data = json.load(f)




### Define the parameters

M = data["M"] # shape: [], definition: The number of inequalities defining the set P

N = data["N"] # shape: [], definition: The ambient space dimension of the set P

A = data["A"] # shape: ['M', 'N'], definition: The coefficients of the linear inequalities defining the set P

B = data["B"] # shape: ['M'], definition: The right-hand side of the inequalities defining the set P



### Define the variables

r = model.addVar(vtype=GRB.CONTINUOUS, name="r")



### Define the constraints

for i in range(M):
    norm_ai = (sum(A[i][j] * A[i][j] for j in range(N))) ** 0.5
    model.addConstr(
        sum(A[i][j] * y[j] for j in range(N)) + r * norm_ai <= B[i]
    )
model.addConstr(r >= 0)


### Define the objective

model.setObjective(r, GRB.MAXIMIZE)


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
