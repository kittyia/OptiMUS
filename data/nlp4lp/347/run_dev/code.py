
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

WestFlow = model.addVars(N, W-1, vtype=GRB.BINARY, name="WestFlow")

NorthFlow = model.addVars(N-1, W, vtype=GRB.BINARY, name="NorthFlow")



### Define the constraints

# Start node (1,1) -> index (0,0)
model.addConstr(WestFlow[0, 0] + NorthFlow[0, 0] == 1)

# Destination node (N,W) -> index (N-1,W-1)
model.addConstr(WestFlow[N-1, W-2] + NorthFlow[N-2, W-1] == 1)

# Flow balance for all other nodes
for n in range(N):
    for w in range(W):
        # Skip start and destination nodes
        if (n == 0 and w == 0) or (n == N-1 and w == W-1):
            continue

        outgoing = 0
        incoming = 0

        # Outgoing flows
        if w < W-1:
            outgoing += WestFlow[n, w]
        if n < N-1:
            outgoing += NorthFlow[n, w]

        # Incoming flows
        if w > 0:
            incoming += WestFlow[n, w-1]
        if n > 0:
            incoming += NorthFlow[n-1, w]

        model.addConstr(outgoing - incoming == 0)
for n in range(N):
    for w in range(W-1):
        model.addConstr(WestFlow[n, w] >= 0)
        model.addConstr(WestFlow[n, w] <= 1)

for n in range(N-1):
    for w in range(W):
        model.addConstr(NorthFlow[n, w] >= 0)
        model.addConstr(NorthFlow[n, w] <= 1)
for n in range(N):
    for w in range(W - 1):
        model.addConstr(WestFlow[n, w] >= 0)

for n in range(N - 1):
    for w in range(W):
        model.addConstr(NorthFlow[n, w] >= 0)


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
