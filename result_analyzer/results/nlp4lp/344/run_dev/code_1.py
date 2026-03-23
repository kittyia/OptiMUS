import os
import numpy as np
import json
from gurobipy import Model, GRB, quicksum


model = Model("OptimizationProblem")

with open("data.json", "r") as f:
    data = json.load(f)


### Define the parameters

NumTerminals = data["NumTerminals"]  # Number of terminals
NumDestinations = data["NumDestinations"]  # Number of destinations
Cost = data["Cost"]  # Cost[i][j]: cost from terminal i to destination j
Demand = data["Demand"]  # Demand at each destination j
Supply = data["Supply"]  # Supply at each terminal i


### Define the variables (nonnegative by default)

amount = model.addVars(
    NumTerminals,
    NumDestinations,
    vtype=GRB.CONTINUOUS,
    lb=0.0,
    name="amount"
)


### Define the constraints

# Supply constraints
for k in range(NumTerminals):
    model.addConstr(
        quicksum(amount[k, j] for j in range(NumDestinations)) == Supply[k]
    )

# Demand constraints
for j in range(NumDestinations):
    model.addConstr(
        quicksum(amount[i, j] for i in range(NumTerminals)) == Demand[j]
    )


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

if model.status == GRB.OPTIMAL:
    print("Optimal Objective Value: ", model.objVal)
    with open("output_solution.txt", "w") as f:
        f.write(str(model.objVal))
else:
    with open("output_solution.txt", "w") as f:
        f.write(str(model.status))
``