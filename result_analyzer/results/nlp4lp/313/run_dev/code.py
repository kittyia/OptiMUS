
import os
import numpy as np
import json 
from gurobipy import Model, GRB, quicksum


model = Model("OptimizationProblem")

with open("data.json", "r") as f:
    data = json.load(f)




### Define the parameters

K = data["K"] # shape: [], definition: Number of mines

MaxWork = data["MaxWork"] # shape: [], definition: Maximum number of mines that can be operated in a year

NumYears = data["NumYears"] # shape: [], definition: Number of years the company will be operating

Royalty = data["Royalty"] # shape: ['K'], definition: Royalty cost for operating mine k

Limit = data["Limit"] # shape: ['K'], definition: Production limit for mine k

Quality = data["Quality"] # shape: ['K'], definition: Quality of the material from mine k

RequiredQuality = data["RequiredQuality"] # shape: ['NumYears'], definition: Required quality of the material for each year

Price = data["Price"] # shape: [], definition: Price per unit of material sold

Discount = data["Discount"] # shape: [], definition: Discount rate on the royalty cost per unit of material sold



### Define the variables

isOperated = model.addVars(K, NumYears, vtype=GRB.BINARY, name="isOperated")

amount = model.addVars(K, NumYears, vtype=GRB.CONTINUOUS, name="amount")



### Define the constraints

for i in range(NumYears):
    model.addConstr(
        sum(isOperated[k, i] for k in range(K)) <= MaxWork
    )
for k in range(K):
    for i in range(NumYears):
        model.addConstr(amount[k, i] >= 0)
        model.addConstr(amount[k, i] <= Limit[k] * isOperated[k, i])
for k in range(K):
    for i in range(NumYears):
        model.addConstr(isOperated[k, i] >= 0)
        model.addConstr(isOperated[k, i] <= 1)
for i in range(NumYears):
    model.addConstr(
        sum(Quality[k] * amount[k, i] for k in range(K)) ==
        RequiredQuality[i] * sum(amount[k, i] for k in range(K))
    )


### Define the objective

model.setObjective(
    quicksum(
        (1 / ((1 + Discount) ** i)) * (
            Price * quicksum(amount[k, i] for k in range(K))
            - quicksum(Royalty[k] * isOperated[k, i] for k in range(K))
        )
        for i in range(NumYears)
    ),
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
