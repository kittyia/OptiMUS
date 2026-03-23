
import os
import numpy as np
import json 
from gurobipy import Model, GRB, quicksum


model = Model("OptimizationProblem")

with open("data.json", "r") as f:
    data = json.load(f)




### Define the parameters

NumSawTypes = data["NumSawTypes"] # shape: [], definition: Number of types of saws available

PlanksCutPerSaw = data["PlanksCutPerSaw"] # shape: ['NumSawTypes'], definition: Number of planks cut per day by each saw type

SawdustPerSaw = data["SawdustPerSaw"] # shape: ['NumSawTypes'], definition: Units of sawdust produced per day by each saw type

MinPlanks = data["MinPlanks"] # shape: [], definition: Minimum number of planks to be cut per day

MaxSawdust = data["MaxSawdust"] # shape: [], definition: Maximum units of sawdust to be produced per day



### Define the variables

NumSaws = model.addVars(NumSawTypes, vtype=GRB.INTEGER, name="NumSaws")



### Define the constraints

model.addConstr(
    sum(PlanksCutPerSaw[i] * NumSaws[i] for i in range(NumSawTypes)) >= MinPlanks
)
model.addConstr(
    sum(SawdustPerSaw[i] * NumSaws[i] for i in range(NumSawTypes)) <= MaxSawdust
)
for i in range(NumSawTypes):
    model.addConstr(NumSaws[i] >= 0)


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
