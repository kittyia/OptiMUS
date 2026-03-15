import os
import numpy as np
import json
from gurobipy import Model, GRB, quicksum


model = Model("OptimizationProblem")

with open("data.json", "r") as f:
    data = json.load(f)


### Define the parameters

PriceFullWeighted = data["PriceFullWeighted"]
PriceSemiWeighted = data["PriceSemiWeighted"]
TotalChipsAvailable = data["TotalChipsAvailable"]
ChipsPerFullWeighted = data["ChipsPerFullWeighted"]
ChipsPerSemiWeighted = data["ChipsPerSemiWeighted"]
TotalProductionHours = data["TotalProductionHours"]
ProductionTimePerKeyboard = data["ProductionTimePerKeyboard"]


### Define the variables

FullWeightedQty = model.addVar(vtype=GRB.INTEGER, lb=0, name="FullWeightedQty")
SemiWeightedQty = model.addVar(vtype=GRB.INTEGER, lb=0, name="SemiWeightedQty")


### Define the constraints

# Chip availability constraint
model.addConstr(
    ChipsPerFullWeighted * FullWeightedQty +
    ChipsPerSemiWeighted * SemiWeightedQty
    <= TotalChipsAvailable,
    name="ChipConstraint"
)

# Production time constraint
model.addConstr(
    ProductionTimePerKeyboard * (FullWeightedQty + SemiWeightedQty)
    <= TotalProductionHours,
    name="TimeConstraint"
)


### Define the objective

model.setObjective(
    PriceFullWeighted * FullWeightedQty +
    PriceSemiWeighted * SemiWeightedQty,
    GRB.MAXIMIZE
)


### Optimize the model

model.optimize()


### Output optimal objective value

if model.status == GRB.OPTIMAL:
    print("Optimal Objective Value: ", model.objVal)
    with open("output_solution.txt", "w") as f:
        f.write(str(model.objVal))
else:
    with open("output_solution.txt", "w") as f:
        f.write(str(model.status))