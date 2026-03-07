
import os
import numpy as np
import json 
from gurobipy import Model, GRB, quicksum


model = Model("OptimizationProblem")

with open("data.json", "r") as f:
    data = json.load(f)




### Define the parameters

NumNodes = data["NumNodes"] # shape: [], definition: Total number of nodes in the network

Capacity = data["Capacity"] # shape: ['NumNodes', 'NumNodes'], definition: Capacity of the communication link from node i to node j in bits per second

Cost = data["Cost"] # shape: ['NumNodes', 'NumNodes'], definition: Cost of transmitting data along the link from node i to node j

NumSourceDestPairs = data["NumSourceDestPairs"] # shape: [], definition: Number of source-destination pairs

SourceDestPairs = data["SourceDestPairs"] # shape: ['NumSourceDestPairs', '2'], definition: Source and destination node indices for each pair

SourceData = data["SourceData"] # shape: ['NumSourceDestPairs'], definition: Amount of data each source needs to send in bits



### Define the variables

Flow = model.addVars(NumSourceDestPairs, NumNodes, NumNodes, vtype=GRB.CONTINUOUS, name="Flow")



### Define the constraints

for k in range(NumSourceDestPairs):
    source = SourceDestPairs[k][0]
    dest = SourceDestPairs[k][1]
    for i in range(NumNodes):
        if i == source:
            b_ki = SourceData[k]
        elif i == dest:
            b_ki = -SourceData[k]
        else:
            b_ki = 0
        
        model.addConstr(
            sum(Flow[k, i, j] for j in range(NumNodes)) -
            sum(Flow[k, j, i] for j in range(NumNodes))
            == b_ki
        )
for i in range(NumNodes):
    for j in range(NumNodes):
        model.addConstr(
            sum(Flow[k, i, j] for k in range(NumSourceDestPairs)) <= Capacity[i][j]
        )
for k in range(NumSourceDestPairs):
    for i in range(NumNodes):
        for j in range(NumNodes):
            model.addConstr(Flow[k, i, j] >= 0)


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
