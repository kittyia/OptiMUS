
import os
import numpy as np
import json 
from gurobipy import Model, GRB, quicksum


model = Model("OptimizationProblem")

with open("data.json", "r") as f:
    data = json.load(f)




### Define the parameters

K = data["K"] # shape: [], definition: Total number of different types of resources

I = data["I"] # shape: [], definition: Number of different requirements for each type of resource

Strength = data["Strength"] # shape: ['K'], definition: Strength of each type of resource

LessOneWaste = data["LessOneWaste"] # shape: ['K'], definition: Value when wastage of resources is less than optimal

MoreOneWaste = data["MoreOneWaste"] # shape: ['K'], definition: Value when wastage of resources is more than optimal

Recruit = data["Recruit"] # shape: ['K'], definition: Number of recruited resources of each type

CostRedundancy = data["CostRedundancy"] # shape: ['K'], definition: Cost of redundancy for each type of resource

NumOverman = data["NumOverman"] # shape: [], definition: Number of overmanned positions

CostOverman = data["CostOverman"] # shape: ['K'], definition: Cost of overmanning for each type of resource

NumShortwork = data["NumShortwork"] # shape: [], definition: Number of shortworked positions

CostShort = data["CostShort"] # shape: ['K'], definition: Cost of short working for each type of resource

Requirement = data["Requirement"] # shape: ['K', 'I'], definition: Manpower requirements for each type of resource over the years



### Define the variables

workforceMore = model.addVars(K, I, vtype=GRB.CONTINUOUS, name="workforceMore")

workforceLess = model.addVars(K, I, vtype=GRB.CONTINUOUS, name="workforceLess")

recruit = model.addVars(K, I, vtype=GRB.CONTINUOUS, name="recruit")

redundancies = model.addVars(K, I, vtype=GRB.CONTINUOUS, name="redundancies")

short = model.addVars(K, I, vtype=GRB.CONTINUOUS, name="short")

overmanning = model.addVars(K, I, vtype=GRB.CONTINUOUS, name="overmanning")



### Define the constraints

for k in range(K):
    # Year 1 (i = 0 in Python indexing)
    model.addConstr(
        workforceMore[k, 0] == (1 - MoreOneWaste[k]) * Strength[k] - redundancies[k, 0]
    )
    model.addConstr(
        workforceLess[k, 0] == recruit[k, 0]
    )
    
    # Years 2,...,I (i = 1,...,I-1 in Python indexing)
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
    model.addConstr(workforceLess[k, 0] == recruit[k, 0])
for k in range(K):
    for i in range(I):
        model.addConstr(recruit[k, i] <= Recruit[k])
for k in range(K):
    for i in range(I):
        model.addConstr(short[k, i] <= NumShortwork)
for k in range(K):
    for i in range(I):
        model.addConstr(
            workforceMore[k, i] + workforceLess[k, i] - 0.5 * short[k, i]
            == Requirement[k][i] + overmanning[k, i]
        )
for i in range(I):
    model.addConstr(
        sum(overmanning[k, i] for k in range(K)) <= NumOverman
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



### Output optimal objective value

print("Optimal Objective Value: ", model.objVal)


if model.status == GRB.OPTIMAL:
    with open("output_solution.txt", "w") as f:
        f.write(str(model.objVal))
    print("Optimal Objective Value: ", model.objVal)
else:
    with open("output_solution.txt", "w") as f:
        f.write(model.status)
