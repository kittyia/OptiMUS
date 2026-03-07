
import os
import numpy as np
import json 
from gurobipy import Model, GRB, quicksum


model = Model("OptimizationProblem")

with open("data.json", "r") as f:
    data = json.load(f)




### Define the parameters

N = data["N"] # shape: [], definition: Number of different shares

Bought = data["Bought"] # shape: ['N'], definition: Amount of each share initially bought

BuyPrice = data["BuyPrice"] # shape: ['N'], definition: Purchase price of each share

CurrentPrice = data["CurrentPrice"] # shape: ['N'], definition: Current market price of each share

FuturePrice = data["FuturePrice"] # shape: ['N'], definition: Expected future market price of each share

TransactionRate = data["TransactionRate"] # shape: [], definition: Transaction cost rate per share sold

TaxRate = data["TaxRate"] # shape: [], definition: Capital gains tax rate on the profit from selling shares

K = data["K"] # shape: [], definition: Amount of money the investor needs to raise



### Define the variables

sell = model.addVars(N, vtype=GRB.CONTINUOUS, name="sell")



### Define the constraints

for i in range(N):
    model.addConstr(sell[i] >= 0)
    model.addConstr(sell[i] <= Bought[i])
model.addConstr(
    sum(
        sell[i] * (
            CurrentPrice[i] * (1 - TransactionRate / 100.0)
            - (TaxRate / 100.0) * max(CurrentPrice[i] - BuyPrice[i], 0)
        )
        for i in range(N)
    ) >= K
)


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
