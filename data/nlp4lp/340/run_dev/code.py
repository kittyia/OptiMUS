
import os
import numpy as np
import json 
from gurobipy import Model, GRB, quicksum


model = Model("OptimizationProblem")

with open("data.json", "r") as f:
    data = json.load(f)




### Define the parameters

M = data["M"] # shape: [], definition: Number of machines

P = data["P"] # shape: [], definition: Number of parts to be produced

TimeRequired = data["TimeRequired"] # shape: ['M', 'P'], definition: Time required to produce a batch of part p on machine m

MachineCosts = data["MachineCosts"] # shape: ['M'], definition: Cost associated with running machine m

Availability = data["Availability"] # shape: ['M'], definition: Availability of machine m per month

Prices = data["Prices"] # shape: ['P'], definition: Selling price of a batch of part p

MinBatches = data["MinBatches"] # shape: ['P'], definition: Minimum number of batches of part p that should be produced



### Define the variables

batches = model.addVars(P, vtype=GRB.CONTINUOUS, name="batches")



### Define the constraints

for m in range(M-2):
    model.addConstr(
        sum(TimeRequired[m][p] * batches[p] for p in range(P)) <= Availability[m]
    )
model.addConstr(
    sum(TimeRequired[M-2][p] * batches[p] for p in range(P)) +
    sum(TimeRequired[M-1][p] * batches[p] for p in range(P))
    <= Availability[M-2] + Availability[M-1]
)
for p in range(P):
    model.addConstr(batches[p] >= MinBatches[p])


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
