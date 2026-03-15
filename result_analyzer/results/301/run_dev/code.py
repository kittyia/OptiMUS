
import os
import numpy as np
import json 
from gurobipy import Model, GRB, quicksum


model = Model("OptimizationProblem")

with open("data.json", "r") as f:
    data = json.load(f)




### Define the parameters

N = data["N"] # shape: [], definition: Number of different currencies

Start = data["Start"] # shape: ['N'], definition: Initial amount of currency i

Limit = data["Limit"] # shape: ['N'], definition: Limit for the number of transactions for currency i

Rate = data["Rate"] # shape: ['N', 'N'], definition: Exchange rate from currency i to currency j



### Define the variables

x = model.addVars(N, N, vtype=GRB.CONTINUOUS, name="x")



### Define the constraints

for i in range(N):
    for j in range(N):
        model.addConstr(x[i, j] >= 0)
for i in range(N):
    model.addConstr(
        Start[i] 
        - sum(x[i, j] for j in range(N)) 
        + sum(Rate[j][i] * x[j, i] for j in range(N)) 
        >= 0
    )
for i in range(N):
    model.addConstr(
        sum(x[i, j] for j in range(N)) + sum(x[j, i] for j in range(N)) <= Limit[i]
    )


### Define the objective

model.setObjective(
    Start[N-1]
    - quicksum(x[N-1, j] for j in range(N))
    + quicksum(Rate[i][N-1] * x[i, N-1] for i in range(N)),
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
