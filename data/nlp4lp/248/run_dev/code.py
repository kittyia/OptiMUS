
import os
import numpy as np
import json 
from gurobipy import Model, GRB, quicksum


model = Model("OptimizationProblem")

with open("data.json", "r") as f:
    data = json.load(f)




### Define the parameters

MaxWater = data["MaxWater"] # shape: [], definition: Maximum units of water available

MaxPollution = data["MaxPollution"] # shape: [], definition: Maximum units of pollution allowed

MetalExtraction = data["MetalExtraction"] # shape: ['NumProcesses'], definition: Amount of metal extracted per unit of process

WaterUsage = data["WaterUsage"] # shape: ['NumProcesses'], definition: Amount of water used per unit of process

PollutionProduction = data["PollutionProduction"] # shape: ['NumProcesses'], definition: Amount of pollution produced per unit of process



### Define the variables

numProcessJ = model.addVar(vtype=GRB.CONTINUOUS, name="numProcessJ")

numProcessP = model.addVar(vtype=GRB.CONTINUOUS, name="numProcessP")



### Define the constraints

model.addConstr(8 * numProcessJ + 6 * numProcessP <= MaxWater)
model.addConstr(numProcessJ >= 0)
model.addConstr(numProcessP >= 0)


### Define the objective

del.setObjective(5 * numProcessJ + 9 * numProcessP, GRB.MAXIMIZE


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
