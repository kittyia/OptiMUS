
import os
import numpy as np
import json 
from gurobipy import Model, GRB, quicksum


model = Model("OptimizationProblem")

with open("data.json", "r") as f:
    data = json.load(f)




### Define the parameters

NumOilTypes = data["NumOilTypes"] # shape: [], definition: Number of different types of crude oil

NumCompounds = data["NumCompounds"] # shape: [], definition: Number of different compounds required to process oil

NetRevenue = data["NetRevenue"] # shape: ['NumOilTypes'], definition: Net revenue per tank for each type of crude oil

CompoundRequirement = data["CompoundRequirement"] # shape: ['NumCompounds', 'NumOilTypes'], definition: Amount of each compound required to process one tank of each type of crude oil

TotalCompoundAvailable = data["TotalCompoundAvailable"] # shape: ['NumCompounds'], definition: Total units of each compound available for processing



### Define the variables

TanksProcessed = model.addVars(NumOilTypes, vtype=GRB.CONTINUOUS, name="TanksProcessed")



### Define the constraints

model.addConstr(
    sum(CompoundRequirement[0][j] * TanksProcessed[j] for j in range(NumOilTypes)) <= 250
)
model.addConstr(
    sum(CompoundRequirement[1][j] * TanksProcessed[j] for j in range(NumOilTypes)) 
    <= TotalCompoundAvailable[1]
)
for i in range(NumOilTypes):
    model.addConstr(TanksProcessed[i] >= 0)


### Define the objective

model.setObjective(quicksum(NetRevenue[i] * TanksProcessed[i] for i in range(NumOilTypes)), GRB.MAXIMIZE)


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
