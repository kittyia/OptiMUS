import os
import numpy as np
import json
from gurobipy import Model, GRB, quicksum


model = Model("OptimizationProblem")

with open("data.json", "r") as f:
    data = json.load(f)


### Define the parameters

# Ensure numeric parameters are integers (fixes TypeError)
K = int(data["K"])
NumIndustries = int(data["NumIndustries"])

ManpowerOne = data["ManpowerOne"]
ManpowerTwo = data["ManpowerTwo"]
Stock = data["Stock"]
Capacity = data["Capacity"]
Demand = data["Demand"]
InputOne = data["InputOne"]
InputTwo = data["InputTwo"]


### Define the variables

produce = model.addVars(NumIndustries, K, vtype=GRB.CONTINUOUS, name="produce")

capacityLevel = model.addVars(NumIndustries, K, vtype=GRB.CONTINUOUS, name="capacityLevel")

buildcapa = model.addVars(NumIndustries, K, vtype=GRB.CONTINUOUS, name="buildcapa")

stockhold = model.addVars(NumIndustries, K, vtype=GRB.CONTINUOUS, name="stockhold")

totalManpower = model.addVars(K, vtype=GRB.CONTINUOUS, name="totalManpower")


### Define the constraints

# Production limited by capacity
for k in range(NumIndustries):
    for t in range(K):
        model.addConstr(produce[k, t] <= capacityLevel[k, t])

# Capacity evolution (capacity increases effective after 2 years)
for k in range(NumIndustries):
    for t in range(K):
        if t >= 2:
            model.addConstr(
                capacityLevel[k, t] ==
                Capacity[k] + quicksum(buildcapa[k, tau] for tau in range(t - 1))
            )
        else:
            model.addConstr(capacityLevel[k, t] == Capacity[k])

# Stock balance constraints
for k in range(NumIndustries):

    # Year 0
    model.addConstr(
        stockhold[k, 0] ==
        Stock[k]
        + produce[k, 0]
        - quicksum(InputOne[i][k] * produce[i, 1] for i in range(NumIndustries))
        - quicksum(InputTwo[i][k] * buildcapa[i, 0] for i in range(NumIndustries))
        - Demand[k]
    )

    # Years 1 to K-2
    for t in range(1, K - 1):
        model.addConstr(
            stockhold[k, t] ==
            stockhold[k, t - 1]
            + produce[k, t]
            - quicksum(InputOne[i][k] * produce[i, t + 1] for i in range(NumIndustries))
            - quicksum(InputTwo[i][k] * buildcapa[i, t] for i in range(NumIndustries))
            - Demand[k]
        )

    # Year K-1
    model.addConstr(
        stockhold[k, K - 1] ==
        stockhold[k, K - 2]
        + produce[k, K - 1]
        - quicksum(InputTwo[i][k] * buildcapa[i, K - 1] for i in range(NumIndustries))
        - Demand[k]
    )

# Initial capacity
for k in range(NumIndustries):
    model.addConstr(capacityLevel[k, 0] == Capacity[k])

# Total manpower per year
for t in range(K):
    model.addConstr(
        totalManpower[t] ==
        quicksum(
            ManpowerOne[k] * produce[k, t] +
            ManpowerTwo[k] * buildcapa[k, t]
            for k in range(NumIndustries)
        )
    )

# Non-negativity
for k in range(NumIndustries):
    for t in range(K):
        model.addConstr(produce[k, t] >= 0)
        model.addConstr(buildcapa[k, t] >= 0)
        model.addConstr(stockhold[k, t] >= 0)


### Define the objective

model.setObjective(quicksum(totalManpower[t] for t in range(K)), GRB.MAXIMIZE)


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