
import os
import numpy as np
import json 
from gurobipy import Model, GRB, quicksum


model = Model("OptimizationProblem")

with open("data.json", "r") as f:
    data = json.load(f)




### Define the parameters

K = data["K"] # shape: [], definition: Number of different spare parts

S = data["S"] # shape: [], definition: Number of machines capable of making the spare parts

Time = data["Time"] # shape: ['K', 'S'], definition: Time taken to make spare part k on machine s

Profit = data["Profit"] # shape: ['K'], definition: Profit obtained from making spare part k

Capacity = data["Capacity"] # shape: ['S'], definition: Capacity of machine s for the spare parts



### Define the variables

quantity = model.addVars(K, vtype=GRB.CONTINUOUS, name="quantity")



### Define the constraints

for s in range(S):
    model.addConstr(
        sum(Time[k][s] * quantity[k] for k in range(K)) <= Capacity[s]
    )
for k in range(K):
    model.addConstr(quantity[k] >= 0)


### Define the objective

model.setObjective(quicksum(Profit[k] * quantity[k] for k in range(K)), GRB.MAXIMIZE)


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
