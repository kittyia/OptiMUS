import os
import numpy as np
import json
from gurobipy import Model, GRB, quicksum


model = Model("OptimizationProblem")

with open("data.json", "r") as f:
    data = json.load(f)


### Define the parameters

UnitsMagnesiumPerGummy = data["UnitsMagnesiumPerGummy"]  # Units of magnesium per gummy
UnitsZincPerGummy = data["UnitsZincPerGummy"]  # Units of zinc per gummy
UnitsMagnesiumPerPill = data["UnitsMagnesiumPerPill"]  # Units of magnesium per pill
UnitsZincPerPill = data["UnitsZincPerPill"]  # Units of zinc per pill
MinimumNumberOfPills = data["MinimumNumberOfPills"]  # Minimum number of pills
MinimumGummiesToPillsRatio = data["MinimumGummiesToPillsRatio"]  # Minimum gummies to pills ratio
MaximumUnitsOfMagnesium = data["MaximumUnitsOfMagnesium"]  # Maximum magnesium consumption


### Define the variables

NumberOfGummies = model.addVar(vtype=GRB.INTEGER, name="NumberOfGummies")
NumberOfPills = model.addVar(vtype=GRB.INTEGER, name="NumberOfPills")


### Define the constraints

model.addConstr(
    UnitsMagnesiumPerGummy * NumberOfGummies
    + UnitsMagnesiumPerPill * NumberOfPills
    <= MaximumUnitsOfMagnesium
)

model.addConstr(NumberOfPills >= MinimumNumberOfPills)

model.addConstr(
    NumberOfGummies >= MinimumGummiesToPillsRatio * NumberOfPills
)


### Define the objective

model.setObjective(
    UnitsZincPerGummy * NumberOfGummies
    + UnitsZincPerPill * NumberOfPills,
    GRB.MAXIMIZE,
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