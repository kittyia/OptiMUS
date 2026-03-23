import os
import numpy as np
import json
from gurobipy import Model, GRB, quicksum


model = Model("OptimizationProblem")

with open("data.json", "r") as f:
    data = json.load(f)


### Define the parameters

K = int(data["K"])  # Number of years
NumIndustries = int(data["NumIndustries"])  # Number of industries

ManpowerOne = data["ManpowerOne"]
ManpowerTwo = data["ManpowerTwo"]
Stock = data["Stock"]
Capacity = data["Capacity"]
Demand = data["Demand"]
InputOne = data["InputOne"]
InputTwo = data["InputTwo"]


### Define the variables

produce = model.addVars(NumIndustries, K, vtype=GRB.CONTINUOUS, name="produce")
capacityAvail = model.addVars(NumIndustries, K, vtype=GRB.CONTINUOUS, name="capacityAvail")
buildcapa = model.addVars(NumIndustries, K, vtype=GRB.CONTINUOUS, name="buildcapa")
stockhold = model.addVars(NumIndustries, K, vtype=GRB.CONTINUOUS, name="stockhold")


### Define the constraints

# Production limited by available capacity
for k in range(NumIndustries):
    for t in range(K):
        model.addConstr(produce[k, t] <= capacityAvail[k, t])

# Capacity evolution (investment becomes available after 2 years)
for k in range(NumIndustries):
    for t in range(K):
        model.addConstr(
            capacityAvail[k, t] ==
            Capacity[k] +
            quicksum(buildcapa[k, tau] for tau in range(0, t - 1))
        )

# Stock balance constraints
for k in range(NumIndustries):
    if K > 1:
        # t = 0
        model.addConstr(
            stockhold[k, 0] ==
            Stock[k] + produce[k, 0]
            - quicksum(
                InputOne[j][k] * produce[j, 1] +
                InputTwo[j][k] * buildcapa[j, 1]
                for j in range(NumIndustries)
            )
            - Demand[k]
        )

        # t = 1, ..., K-2
        for t in range(1, K - 1):
            model.addConstr(
                stockhold[k, t] ==
                stockhold[k, t - 1] + produce[k, t]
                - quicksum(
                    InputOne[j][k] * produce[j, t + 1] +
                    InputTwo[j][k] * buildcapa[j, t + 1]
                    for j in range(NumIndustries)
                )
                - Demand[k]
            )

        # t = K-1
        model.addConstr(
            stockhold[k, K - 1] ==
            stockhold[k, K - 2] + produce[k, K - 1]
            - Demand[k]
        )
    else:
        model.addConstr(
            stockhold[k, 0] ==
            Stock[k] + produce[k, 0]
            - Demand[k]
        )

# Non-negativity constraints
for k in range(NumIndustries):
    for t in range(K):
        model.addConstr(stockhold[k, t] >= 0)
        model.addConstr(produce[k, t] >= 0)
        model.addConstr(buildcapa[k, t] >= 0)


### Define the objective

model.setObjective(
    quicksum(
        ManpowerOne[k] * produce[k, t] +
        ManpowerTwo[k] * buildcapa[k, t]
        for k in range(NumIndustries)
        for t in range(K)
    ),
    GRB.MAXIMIZE
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