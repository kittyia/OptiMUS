
import os
import numpy as np
import json 
from gurobipy import Model, GRB, quicksum


model = Model("OptimizationProblem")

with open("data.json", "r") as f:
    data = json.load(f)




### Define the parameters

M = data["M"] # shape: [], definition: Number of months

I = data["I"] # shape: [], definition: Number of different items

BuyPrice = data["BuyPrice"] # shape: ['M', 'I'], definition: Month m buy price of item i

SellPrice = data["SellPrice"] # shape: [], definition: Sell price of the products after refining

IsVegetable = data["IsVegetable"] # shape: ['I'], definition: Indicator whether item i is a vegetable

MaxVegetableRefiningPerMonth = data["MaxVegetableRefiningPerMonth"] # shape: [], definition: Maximum refining capability for vegetables per month

MaxNonVegetableRefiningPerMonth = data["MaxNonVegetableRefiningPerMonth"] # shape: [], definition: Maximum refining capability for non-vegetables per month

StorageSize = data["StorageSize"] # shape: [], definition: Size of the storage

StorageCost = data["StorageCost"] # shape: [], definition: Cost for storing items per month

MaxHardness = data["MaxHardness"] # shape: [], definition: The maximum hardness allowed for the products after refining

MinHardness = data["MinHardness"] # shape: [], definition: The minimum hardness required for the products after refining

Hardness = data["Hardness"] # shape: ['I'], definition: Hardness of item i

InitialAmount = data["InitialAmount"] # shape: [], definition: Initial amount of items in storage at the beginning of the planning horizon



### Define the variables

storage = model.addVars(I, M, vtype=GRB.CONTINUOUS, name="storage")

buy = model.addVars(I, M, vtype=GRB.CONTINUOUS, name="buy")

refine = model.addVars(I, M, vtype=GRB.CONTINUOUS, name="refine")



### Define the constraints

for i in range(I):  
    for m in range(M):  
        if m == 0:  
            model.addConstr(storage[i, m] == InitialAmount + buy[i, m] - refine[i, m])  
        else:  
            model.addConstr(storage[i, m] == storage[i, m-1] + buy[i, m] - refine[i, m])
for i in range(I):
    model.addConstr(storage[i, 0] == InitialAmount)
for i in range(I):
    model.addConstr(storage[i, M-1] == InitialAmount)
for i in range(I):
    for m in range(M):
        model.addConstr(storage[i, m] <= StorageSize)
for m in range(M):
    model.addConstr(
        sum(IsVegetable[i] * refine[i, m] for i in range(I))
        <= MaxVegetableRefiningPerMonth
    )
for m in range(M):
    model.addConstr(
        sum(refine[i, m] for i in range(I) if IsVegetable[i] == 0)
        <= MaxNonVegetableRefiningPerMonth
    )
for m in range(M):
    total_refine_m = sum(refine[i, m] for i in range(I))
    weighted_hardness_m = sum(Hardness[i] * refine[i, m] for i in range(I))
    
    model.addConstr(MinHardness * total_refine_m <= weighted_hardness_m)
    model.addConstr(weighted_hardness_m <= MaxHardness * total_refine_m)
for i in range(I):
    for m in range(M):
        model.addConstr(buy[i, m] >= 0)
for i in range(I):
    for m in range(M):
        model.addConstr(refine[i, m] >= 0)
for i in range(I):
    for m in range(M):
        model.addConstr(storage[i, m] >= 0)


### Define the objective

model.setObjective(
    quicksum(
        SellPrice * refine[i, m]
        - BuyPrice[m][i] * buy[i, m]
        - StorageCost * storage[i, m]
        for m in range(M)
        for i in range(I)
    ),
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
