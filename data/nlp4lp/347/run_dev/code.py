
import os
import numpy as np
import json 
from gurobipy import Model, GRB, quicksum


model = Model("OptimizationProblem")

with open("data.json", "r") as f:
    data = json.load(f)




### Define the parameters

N = data["N"] # shape: [], definition: Number of east-west streets

W = data["W"] # shape: [], definition: Number of north-south streets

WestTime = data["WestTime"] # shape: ['N', 'W'], definition: Time to cross street segment going west, for given street n and segment w

NorthTime = data["NorthTime"] # shape: ['W', 'N'], definition: Time to cross street segment going north, for given street n and segment w



### Define the variables

xWest = model.addVars(N, W-1, vtype=GRB.CONTINUOUS, name="xWest")

xNorth = model.addVars(N-1, W, vtype=GRB.CONTINUOUS, name="xNorth")



### Define the constraints

for n in range(N):
    for w in range(W):
        inflow = 0
        outflow = 0

        if w > 0:
            inflow += xWest[n, w-1]
        if n > 0:
            inflow += xNorth[n-1, w]

        if w < W-1:
            outflow += xWest[n, w]
        if n < N-1:
            outflow += xNorth[n, w]

        if n == 0 and w == 0:
            rhs = -1
        elif n == N-1 and w == W-1:
            rhs = 1
        else:
            rhs = 0

        model.addConstr(inflow - outflow == rhs)
for n in range(N):
    for w in range(W-1):
        model.addConstr(xWest[n, w] >= 0)

for n in range(N-1):
    for w in range(W):
        model.addConstr(xNorth[n, w] >= 0)


### Define the objective

model.setObjective(
    quicksum(WestTime[n][w] * xWest[n, w] for n in range(N) for w in range(W-1)) +
    quicksum(NorthTime[n][w] * xNorth[n, w] for n in range(N-1) for w in range(W)),
    GRB.MINIMIZE
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
