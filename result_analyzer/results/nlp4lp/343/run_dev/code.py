
import os
import numpy as np
import json 
from gurobipy import Model, GRB, quicksum


model = Model("OptimizationProblem")

with open("data.json", "r") as f:
    data = json.load(f)




### Define the parameters

P = data["P"] # shape: [], definition: Number of power plants

C = data["C"] # shape: [], definition: Number of cities

Supply = data["Supply"] # shape: ['P'], definition: Electricity supply capacity of power plant p

Demand = data["Demand"] # shape: ['C'], definition: Electricity demand of city c

TransmissionCosts = data["TransmissionCosts"] # shape: ['P', 'C'], definition: Transmission cost from power plant p to city c



### Define the variables

send = model.addVars(P, C, vtype=GRB.CONTINUOUS, name="send")



### Define the constraints

for p in range(P):
    model.addConstr(
        sum(send[p, c] for c in range(C)) <= Supply[p]
    )
for c in range(C):
    model.addConstr(sum(send[p, c] for p in range(P)) == Demand[c])
for p in range(P):
    for c in range(C):
        model.addConstr(send[p, c] >= 0)


### Define the objective

model.setObjective(
    quicksum(TransmissionCosts[p][c] * send[p, c] 
             for p in range(P) 
             for c in range(C)),
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
