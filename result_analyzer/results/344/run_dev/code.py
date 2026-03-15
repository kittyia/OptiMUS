
import os
import numpy as np
import json 
from gurobipy import Model, GRB, quicksum


model = Model("OptimizationProblem")

with open("data.json", "r") as f:
    data = json.load(f)




### Define the parameters

NumTerminals = data["NumTerminals"] # shape: [], definition: Number of terminals

NumDestinations = data["NumDestinations"] # shape: [], definition: Number of destinations

Cost = data["Cost"] # shape: ['NumTerminals', 'NumDestinations'], definition: Cost of transportation for route from terminal i to destination j

Demand = data["Demand"] # shape: ['NumDestinations'], definition: Demand at each destination

Supply = data["Supply"] # shape: ['NumTerminals'], definition: Supply at each terminal



### Define the variables

amount = model.addVars(NumTerminals, NumDestinations, vtype=GRB.CONTINUOUS, name="amount")



### Define the constraints

for k in range(NumTerminals):
    model.addConstr(
        sum(amount[k, j] for j in range(NumDestinations)) <= Supply[k]
    )
for l in range(NumDestinations):
    model.addConstr(
        sum(amount[k, l] for k in range(NumTerminals)) >= Demand[l]
    )
for k in range(NumTerminals):
    for j in range(NumDestinations):
        model.addConstr(amount[k, j] >= 0)


### Define the objective

model.setObjective(
    quicksum(Cost[i][j] * amount[i, j] 
             for i in range(NumTerminals) 
             for j in range(NumDestinations)),
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
