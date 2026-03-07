
import os
import numpy as np
import json 
from gurobipy import Model, GRB, quicksum


model = Model("OptimizationProblem")

with open("data.json", "r") as f:
    data = json.load(f)




### Define the parameters

N = data["N"] # shape: [], definition: Number of different raw materials

M = data["M"] # shape: [], definition: Number of different products

Available = data["Available"] # shape: ['N'], definition: Amount of raw material i available

Requirements = data["Requirements"] # shape: ['N', 'M'], definition: Amount of raw material i required to produce one unit of product j

Prices = data["Prices"] # shape: ['M'], definition: Price at which product j can be sold

Costs = data["Costs"] # shape: ['M'], definition: Cost of producing one unit of product j

Demands = data["Demands"] # shape: ['M'], definition: Demand for product j



### Define the variables

amount = model.addVars(M, vtype=GRB.CONTINUOUS, name="amount")



### Define the constraints

for i in range(N):
    model.addConstr(
        sum(Requirements[i][j] * amount[j] for j in range(M)) <= Available[i]
    )
for j in range(M):
    model.addConstr(amount[j] >= 0)
    model.addConstr(amount[j] <= Demands[j])


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
