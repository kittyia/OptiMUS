import os
import numpy as np
import json 
from gurobipy import Model, GRB, quicksum


model = Model("OptimizationProblem")

with open("data.json", "r") as f:
    data = json.load(f)


### Define the parameters

K = data["K"]
I = data["I"]

Strength = data["Strength"]
LessOneWaste = data["LessOneWaste"]
MoreOneWaste = data["MoreOneWaste"]
Recruit = data["Recruit"]
CostRedundancy = data["CostRedundancy"]
NumOverman = data["NumOverman"]
CostOverman = data["CostOverman"]
NumShortwork = data["NumShortwork"]
CostShort = data["CostShort"]
Requirement = data["Requirement"]


### Define the variables

workforceMore = model.addVars(K, I, vtype=GRB.CONTINUOUS, name="workforceMore")
workforceLess = model.addVars(K, I, vtype=GRB.CONTINUOUS, name="workforceLess")
recruit = model.addVars(K, I, vtype=GRB.CONTINUOUS, name="recruit")
redundancies = model.addVars(K, I, vtype=GRB.CONTINUOUS, name="redundancies")
short = model.addVars(K, I, vtype=GRB.CONTINUOUS, name="short")
overmanning = model.addVars(K, I, vtype=GRB.CONTINUOUS, name="overmanning")


### Define the constraints

for k in range(K):
    # Year 1
    model.addConstr(
        workforceMore[k, 0] == (1 - MoreOneWaste[k]) * Strength[k] - redundancies[k, 0]
    )
    model.addConstr(
        workforceLess[k, 0] == recruit[k, 0]
    )
    
    # Years 2,...,I
    for i in range(1, I):
        model.addConstr(
            workforceMore[k, i] == 
            (1 - MoreOneWaste[k]) * workforceMore[k, i-1] +
            (1 - LessOneWaste[k]) * workforceLess[k, i-1] -
            redundancies[k, i]
        )
        model.addConstr(
            workforceLess[k, i] == recruit[k, i]
        )

for k in range(K):
    model.addConstr(workforceMore[k, 0] + redundancies[k, 0] == Strength[k])

for k in range(K):
    for i in range(I):
        model.addConstr(recruit[k, i] <= Recruit[k])
        model.addConstr(short[k, i] <= NumShortwork)

for k in range(K):
    for i in range(I):
        model.addConstr(
            workforceMore[k, i] + workforceLess[k, i] - 0.5 * short[k, i]
            == Requirement[k][i] + overmanning[k, i]
        )

for i in range(I):
    model.addConstr(
        quicksum(overmanning[k, i] for k in range(K)) <= NumOverman
    )

for k in range(K):
    for i in range(I):
        model.addConstr(recruit[k, i] >= 0)
        model.addConstr(redundancies[k, i] >= 0)
        model.addConstr(overmanning[k, i] >= 0)
        model.addConstr(short[k, i] >= 0)


### Define the objective

model.setObjective(
    quicksum(redundancies[k, i] for k in range(K) for i in range(I)),
    GRB.MINIMIZE
)


### Optimize the model

model.optimize()


### Output optimal objective value safely

if model.status == GRB.OPTIMAL:
    print("Optimal Objective Value: ", model.ObjVal)
    with open("output_solution.txt", "w") as f:
        f.write(str(model.ObjVal))
else:
    print("Optimization was not successful. Status code:", model.status)
    with open("output_solution.txt", "w") as f:
        f.write(str(model.status))