
import os
import numpy as np
import json 
from gurobipy import Model, GRB, quicksum


model = Model("OptimizationProblem")

with open("data.json", "r") as f:
    data = json.load(f)




### Define the parameters

GoldRequiredProcessA = data["GoldRequiredProcessA"] # shape: [], definition: Amount of gold required to run Process A once

WireRequiredProcessA = data["WireRequiredProcessA"] # shape: [], definition: Number of wires required to run Process A once

CoinsPlatedProcessA = data["CoinsPlatedProcessA"] # shape: [], definition: Number of coins plated per execution of Process A

GoldRequiredProcessB = data["GoldRequiredProcessB"] # shape: [], definition: Amount of gold required to run Process B once

WireRequiredProcessB = data["WireRequiredProcessB"] # shape: [], definition: Number of wires required to run Process B once

CoinsPlatedProcessB = data["CoinsPlatedProcessB"] # shape: [], definition: Number of coins plated per execution of Process B

TotalGoldAvailable = data["TotalGoldAvailable"] # shape: [], definition: Total amount of gold available

TotalWiresAvailable = data["TotalWiresAvailable"] # shape: [], definition: Total number of wires available



### Define the variables

ProcessARuns = model.addVar(vtype=GRB.INTEGER, name="ProcessARuns")

ProcessBRuns = model.addVar(vtype=GRB.INTEGER, name="ProcessBRuns")



### Define the constraints

model.addConstr(WireRequiredProcessA * ProcessARuns + WireRequiredProcessB * ProcessBRuns <= TotalWiresAvailable)
model.addConstr(ProcessARuns >= 0)
model.addConstr(ProcessBRuns >= 0)


### Define the objective

model.setObjective(
    CoinsPlatedProcessA * ProcessARuns + CoinsPlatedProcessB * ProcessBRuns,
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
