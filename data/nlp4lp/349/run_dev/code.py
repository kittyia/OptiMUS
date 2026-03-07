
import os
import numpy as np
import json 
from gurobipy import Model, GRB, quicksum


model = Model("OptimizationProblem")

with open("data.json", "r") as f:
    data = json.load(f)




### Define the parameters

M = data["M"] # shape: [], definition: The number of machines available

P = data["P"] # shape: [], definition: The number of types of parts to produce

TimeRequired = data["TimeRequired"] # shape: ['M', 'P'], definition: The time required to produce a batch on machine m for part p

MachineCosts = data["MachineCosts"] # shape: ['M'], definition: The cost of operating machine m for a month

Availability = data["Availability"] # shape: ['M'], definition: The time each machine m is available for production each month

Prices = data["Prices"] # shape: ['P'], definition: The price at which part p can be sold

SetupTime = data["SetupTime"] # shape: ['P'], definition: The setup time required before producing a batch of part p



### Define the variables

batches = model.addVars(P, vtype=GRB.INTEGER, name="batches")

setupFlags = model.addVars(P, vtype=GRB.BINARY, name="setupFlags")



### Define the constraints

for m in range(1, M):
    model.addConstr(
        sum(TimeRequired[m][p] * batches[p] for p in range(P)) 
        <= Availability[m]
    )
model.addConstr(
    sum(TimeRequired[0][p] * batches[p] + SetupTime[p] * setupFlags[p] for p in range(P))
    <= Availability[0]
)
for p in range(P):
    model.addConstr(batches[p] <= BigM * setupFlags[p])
for p in range(P):
    model.addConstr(batches[p] >= 0)
for p in range(P):
    model.addConstr(setupFlags[p] >= 0)
    model.addConstr(setupFlags[p] <= 1)


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
