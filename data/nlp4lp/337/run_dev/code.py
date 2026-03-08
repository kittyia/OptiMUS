
import os
import numpy as np
import json 
from gurobipy import Model, GRB, quicksum


model = Model("OptimizationProblem")

with open("data.json", "r") as f:
    data = json.load(f)




### Define the parameters

A = data["A"] # shape: [], definition: Total number of different alloys

S = data["S"] # shape: [], definition: Total number of different steel types

AvailableAlloy = data["AvailableAlloy"] # shape: ['A'], definition: Available amount of alloy a

CarbonContent = data["CarbonContent"] # shape: ['A'], definition: Carbon content of alloy a

NickelContent = data["NickelContent"] # shape: ['A'], definition: Nickel content of alloy a

AlloyPrice = data["AlloyPrice"] # shape: ['A'], definition: Price of alloy a

SteelPrice = data["SteelPrice"] # shape: ['S'], definition: Price of steel type s

CarbonMin = data["CarbonMin"] # shape: ['S'], definition: Minimum required carbon content for steel type s

NickelMax = data["NickelMax"] # shape: ['S'], definition: Maximum allowed nickel content for steel type s



### Define the variables

alloyUse = model.addVars(A, S, vtype=GRB.CONTINUOUS, name="alloyUse")

totalSteel = model.addVars(S, vtype=GRB.CONTINUOUS, name="totalSteel")



### Define the constraints

for s in range(S):
    model.addConstr(
        totalSteel[s] == sum(alloyUse[a, s] for a in range(A))
    )
for a in range(A):
    model.addConstr(
        sum(alloyUse[a, s] for s in range(S)) <= AvailableAlloy[a]
    )
for s in range(S):
    model.addConstr(
        sum(CarbonContent[a] * alloyUse[a, s] for a in range(A)) 
        >= CarbonMin[s] * totalSteel[s]
    )
for s in range(S):
    model.addConstr(
        sum(NickelContent[a] * alloyUse[a, s] for a in range(A))
        <= NickelMax[s] * totalSteel[s]
    )
for s in range(S):
    model.addConstr(alloyUse[0, s] <= 0.4 * totalSteel[s])
for a in range(A):
    for s in range(S):
        model.addConstr(alloyUse[a, s] >= 0)


### Define the objective

model.setObjective(
    quicksum(SteelPrice[s] * totalSteel[s] for s in range(S))
    - quicksum(AlloyPrice[a] * alloyUse[a, s] for a in range(A) for s in range(S)),
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
