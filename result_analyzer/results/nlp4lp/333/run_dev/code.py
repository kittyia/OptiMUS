
import os
import numpy as np
import json 
from gurobipy import Model, GRB, quicksum


model = Model("OptimizationProblem")

with open("data.json", "r") as f:
    data = json.load(f)




### Define the parameters

I = data["I"] # shape: [], definition: Number of depots

J = data["J"] # shape: [], definition: Number of ports

Price = data["Price"] # shape: [], definition: Cost per unit distance for transporting goods

Distance = data["Distance"] # shape: ['I', 'J'], definition: Distance between depot i and port j

NumDepot = data["NumDepot"] # shape: ['I'], definition: Number of containers available in depot i

NumPort = data["NumPort"] # shape: ['J'], definition: Container requirement in port j



### Define the variables

number = model.addVars(I, J, vtype=GRB.CONTINUOUS, name="number")



### Define the constraints

for i in range(I):
    model.addConstr(
        sum(number[i, j] for j in range(J)) <= NumDepot[i]
    )
for j in range(J):
    model.addConstr(
        sum(number[i, j] for i in range(I)) == NumPort[j]
    )
for i in range(I):
    for j in range(J):
        model.addConstr(number[i, j] >= 0)


### Define the objective

model.setObjective(
    quicksum((Price * Distance[i][j] / 2.0) * number[i, j]
             for i in range(I)
             for j in range(J)),
    GRB.MINIMIZE
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
