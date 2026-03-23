
import os
import numpy as np
import json 
from gurobipy import Model, GRB, quicksum


model = Model("OptimizationProblem")

with open("data.json", "r") as f:
    data = json.load(f)




### Define the parameters

PercentageCatPawMix1 = data["PercentageCatPawMix1"] # shape: [], definition: Percentage of cat paw snacks in the first mix

PercentageCatPawMix2 = data["PercentageCatPawMix2"] # shape: [], definition: Percentage of cat paw snacks in the second mix

AvailableCatPawKg = data["AvailableCatPawKg"] # shape: [], definition: Available kilograms of cat paw snacks

AvailableGoldSharkKg = data["AvailableGoldSharkKg"] # shape: [], definition: Available kilograms of gold shark snacks

ProfitPerKgMix1 = data["ProfitPerKgMix1"] # shape: [], definition: Profit per kilogram of the first mix

ProfitPerKgMix2 = data["ProfitPerKgMix2"] # shape: [], definition: Profit per kilogram of the second mix



### Define the variables

Mix1Kg = model.addVar(vtype=GRB.CONTINUOUS, name="Mix1Kg")

Mix2Kg = model.addVar(vtype=GRB.CONTINUOUS, name="Mix2Kg")



### Define the constraints

model.addConstr((PercentageCatPawMix1 / 100.0) * Mix1Kg + (PercentageCatPawMix2 / 100.0) * Mix2Kg <= AvailableCatPawKg)
model.addConstr(0.80 * Mix1Kg + 0.65 * Mix2Kg <= AvailableGoldSharkKg)
model.addConstr(Mix1Kg >= 0)
model.addConstr(Mix2Kg >= 0)


### Define the objective

model.setObjective(ProfitPerKgMix1 * Mix1Kg + ProfitPerKgMix2 * Mix2Kg, GRB.MAXIMIZE)


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
