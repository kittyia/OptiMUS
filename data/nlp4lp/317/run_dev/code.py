
import os
import numpy as np
import json 
from gurobipy import Model, GRB, quicksum


model = Model("OptimizationProblem")

with open("data.json", "r") as f:
    data = json.load(f)




### Define the parameters

K = data["K"] # shape: [], definition: The number of years over which the total manpower requirement is maximized

NumIndustries = data["NumIndustries"] # shape: [], definition: The number of industries in the economy

ManpowerOne = data["ManpowerOne"] # shape: ['NumIndustries'], definition: Manpower requirements for operations one in each industry

ManpowerTwo = data["ManpowerTwo"] # shape: ['NumIndustries'], definition: Manpower requirements for operations two in each industry

Stock = data["Stock"] # shape: ['NumIndustries'], definition: Stock level of product k at the beginning of the year

Capacity = data["Capacity"] # shape: ['NumIndustries'], definition: Production capacity for product k for the year

Demand = data["Demand"] # shape: ['NumIndustries'], definition: Demand for product k for the year

InputOne = data["InputOne"] # shape: ['NumIndustries', 'NumIndustries'], definition: Input one coefficient for product k with respect to product j

InputTwo = data["InputTwo"] # shape: ['NumIndustries', 'NumIndustries'], definition: Input two coefficient for product k with respect to product j



### Define the variables

produce = model.addVars(NumIndustries, K, vtype=GRB.CONTINUOUS, name="produce")

capacityLevel = model.addVars(NumIndustries, K, vtype=GRB.CONTINUOUS, name="capacityLevel")

buildcapa = model.addVars(NumIndustries, K, vtype=GRB.CONTINUOUS, name="buildcapa")

stockhold = model.addVars(NumIndustries, K, vtype=GRB.CONTINUOUS, name="stockhold")

totalManpower = model.addVars(K, vtype=GRB.CONTINUOUS, name="totalManpower")



### Define the constraints

for k in range(NumIndustries):
    for t in range(K):
        model.addConstr(produce[k, t] <= capacityLevel[k, t])
for k in range(NumIndustries):
    for t in range(K):
        if t >= 2:
            model.addConstr(
                capacityLevel[k, t] == Capacity[k] + sum(buildcapa[k, tau] for tau in range(t-1))
            )
        else:
            model.addConstr(
                capacityLevel[k, t] == Capacity[k]
            )
for k in range(NumIndustries):
    # Year 1 (t = 0 in Python indexing)
    model.addConstr(
        stockhold[k, 0] ==
        Stock[k]
        + produce[k, 0]
        - sum(InputOne[i][k] * produce[i, 1] for i in range(NumIndustries))
        - sum(InputTwo[i][k] * buildcapa[i, 0] for i in range(NumIndustries))
        - Demand[k]
    )

    # Years 2 to K-1 (t = 1 to K-2 in Python indexing)
    for t in range(1, K - 1):
        model.addConstr(
            stockhold[k, t] ==
            stockhold[k, t - 1]
            + produce[k, t]
            - sum(InputOne[i][k] * produce[i, t + 1] for i in range(NumIndustries))
            - sum(InputTwo[i][k] * buildcapa[i, t] for i in range(NumIndustries))
            - Demand[k]
        )

    # Year K (t = K-1 in Python indexing)
    model.addConstr(
        stockhold[k, K - 1] ==
        stockhold[k, K - 2]
        + produce[k, K - 1]
        - sum(InputTwo[i][k] * buildcapa[i, K - 1] for i in range(NumIndustries))
        - Demand[k]
    )
for j in range(NumIndustries):
    for t in range(K-1):
        model.addConstr(
            sum(InputOne[k][j] * produce[k, t+1] for k in range(NumIndustries))
            == sum(InputOne[k][j] * produce[k, t+1] for k in range(NumIndustries))
        )
for k in range(NumIndustries):
    model.addConstr(capacityLevel[k, 0] == Capacity[k])
for t in range(K):
    model.addConstr(
        totalManpower[t] == sum(
            ManpowerOne[k] * produce[k, t] + ManpowerTwo[k] * buildcapa[k, t]
            for k in range(NumIndustries)
        )
    )
for k in range(NumIndustries):
    for t in range(K):
        model.addConstr(produce[k, t] >= 0)
for k in range(NumIndustries):
    for t in range(K):
        model.addConstr(buildcapa[k, t] >= 0)
for k in range(NumIndustries):
    for t in range(K):
        model.addConstr(stockhold[k, t] >= 0)


### Define the objective

model.setObjective(quicksum(totalManpower[t] for t in range(K)), GRB.MAXIMIZE)


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
