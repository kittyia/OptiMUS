
import os
import numpy as np
import json 
from gurobipy import Model, GRB, quicksum


model = Model("OptimizationProblem")

with open("data.json", "r") as f:
    data = json.load(f)




### Define the parameters

K = data["K"] # shape: [], definition: Number of different types of food

M = data["M"] # shape: [], definition: Number of nutrients to consider

Price = data["Price"] # shape: ['K'], definition: Price of food k

Demand = data["Demand"] # shape: ['M'], definition: Demand for nutrient m

Nutrition = data["Nutrition"] # shape: ['K', 'M'], definition: Amount of nutrient m in food k



### Define the variables

quantity = model.addVars(K, vtype=GRB.CONTINUOUS, name="quantity")



### Define the constraints

for m in range(M):
    model.addConstr(
        sum(Nutrition[k][m] * quantity[k] for k in range(K)) >= Demand[m]
    )
for k in range(K):
    model.addConstr(quantity[k] >= 0)


### Define the objective

model.setObjective(quicksum(Price[k] * quantity[k] for k in range(K)), GRB.MINIMIZE)


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
