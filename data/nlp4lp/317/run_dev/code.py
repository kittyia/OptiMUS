
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

capacityAvail = model.addVars(NumIndustries, K, vtype=GRB.CONTINUOUS, name="capacityAvail")

buildcapa = model.addVars(NumIndustries, K, vtype=GRB.CONTINUOUS, name="buildcapa")

stockhold = model.addVars(NumIndustries, K, vtype=GRB.CONTINUOUS, name="stockhold")



### Define the constraints

for k in range(NumIndustries):
    for t in range(K):
        model.addConstr(produce[k, t] <= capacityAvail[k, t])
for k in range(NumIndustries):
    for t in range(K):
        model.addConstr(
            capacityAvail[k, t] == Capacity[k] + 
            sum(buildcapa[k, tau] for tau in range(0, t-1))
        )
for k in range(NumIndustries):
    if K > 1:
        # t = 1 (index 0)
        model.addConstr(
            stockhold[k, 0] ==
            Stock[k] + produce[k, 0]
            - sum(
                InputOne[j][k] * produce[j, 1] +
                InputTwo[j][k] * buildcapa[j, 1]
                for j in range(NumIndustries)
            )
            - Demand[k]
        )

        # t = 2, ..., K-1 (indices 1 to K-2)
        for t in range(1, K - 1):
            model.addConstr(
                stockhold[k, t] ==
                stockhold[k, t - 1] + produce[k, t]
                - sum(
                    InputOne[j][k] * produce[j, t + 1] +
                    InputTwo[j][k] * buildcapa[j, t + 1]
                    for j in range(NumIndustries)
                )
                - Demand[k]
            )

        # t = K (index K-1)
        model.addConstr(
            stockhold[k, K - 1] ==
            stockhold[k, K - 2] + produce[k, K - 1]
            - Demand[k]
        )
    else:
        # Special case when K = 1
        model.addConstr(
            stockhold[k, 0] ==
            Stock[k] + produce[k, 0]
            - Demand[k]
        )
for k in range(NumIndustries):
    for t in range(K):
        model.addConstr(stockhold[k, t] >= 0)
for k in range(NumIndustries):
    for t in range(K):
        model.addConstr(produce[k, t] >= 0)
for k in range(NumIndustries):
    for t in range(K):
        model.addConstr(buildcapa[k, t] >= 0)


### Define the objective

model.setObjective(
    quicksum(
        ManpowerOne[k] * produce[k, t] + ManpowerTwo[k] * buildcapa[k, t]
        for k in range(NumIndustries)
        for t in range(K)
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
