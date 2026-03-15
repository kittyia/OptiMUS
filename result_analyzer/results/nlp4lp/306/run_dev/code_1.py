import os
import numpy as np
import json
from gurobipy import Model, GRB, quicksum

model = Model("OptimizationProblem")

with open("data.json", "r") as f:
    data = json.load(f)

### Define the parameters

N = data["N"]

Bought = data["Bought"]
BuyPrice = data["BuyPrice"]
CurrentPrice = data["CurrentPrice"]
FuturePrice = data["FuturePrice"]

TransactionRate = data["TransactionRate"]
TaxRate = data["TaxRate"]

K = data["K"]

### Define the variables

sell = model.addVars(N, lb=0.0, name="sell")

### Define the constraints

# Cannot sell more than owned
for i in range(N):
    model.addConstr(sell[i] <= Bought[i])

# Net cash raised constraint
model.addConstr(
    quicksum(
        sell[i] * CurrentPrice[i] * (1 - TransactionRate / 100.0)
        - (TaxRate / 100.0) * sell[i] * max(CurrentPrice[i] - BuyPrice[i], 0)
        for i in range(N)
    ) >= K
)

### Define the objective

model.setObjective(
    quicksum(FuturePrice[i] * (Bought[i] - sell[i]) for i in range(N)),
    GRB.MAXIMIZE
)

### Optimize the model

model.optimize()

### Output optimal objective value

if model.status == GRB.OPTIMAL:
    print("Optimal Objective Value:", model.objVal)
    with open("output_solution.txt", "w") as f:
        f.write(str(model.objVal))
else:
    with open("output_solution.txt", "w") as f:
        f.write(str(model.status))