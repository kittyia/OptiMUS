
import os
import numpy as np
import json 
from gurobipy import Model, GRB, quicksum


model = Model("OptimizationProblem")

with open("data.json", "r") as f:
    data = json.load(f)




### Define the parameters

PriceFullWeighted = data["PriceFullWeighted"] # shape: [], definition: Price of the full-weighted keyboard

PriceSemiWeighted = data["PriceSemiWeighted"] # shape: [], definition: Price of the semi-weighted keyboard

TotalChipsAvailable = data["TotalChipsAvailable"] # shape: [], definition: Total oscillator chips available per day

ChipsPerFullWeighted = data["ChipsPerFullWeighted"] # shape: [], definition: Number of oscillator chips required per full-weighted keyboard

ChipsPerSemiWeighted = data["ChipsPerSemiWeighted"] # shape: [], definition: Number of oscillator chips required per semi-weighted keyboard

TotalProductionHours = data["TotalProductionHours"] # shape: [], definition: Total production hours available per day

ProductionTimePerKeyboard = data["ProductionTimePerKeyboard"] # shape: [], definition: Production time required to manufacture one keyboard



### Define the variables

FullWeightedQty = model.addVar(vtype=GRB.INTEGER, name="FullWeightedQty")

SemiWeightedQty = model.addVar(vtype=GRB.INTEGER, name="SemiWeightedQty")



### Define the constraints

model.addConstr(FullWeightedQty + SemiWeightedQty <= 5)
model.addConstr(FullWeightedQty >= 0)
model.addConstr(SemiWeightedQty >= 0)


### Define the objective

del.setObjective(
    PriceFullWeighted * FullWeightedQty +
    PriceSemiWeighted * SemiWeightedQty,
    GRB.MAXIMIZE


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
