
import os
import numpy as np
import json 
from gurobipy import Model, GRB, quicksum


model = Model("OptimizationProblem")

with open("data.json", "r") as f:
    data = json.load(f)




### Define the parameters

UnitsMagnesiumPerGummy = data["UnitsMagnesiumPerGummy"] # shape: [], definition: Units of magnesium per gummy

UnitsZincPerGummy = data["UnitsZincPerGummy"] # shape: [], definition: Units of zinc per gummy

UnitsMagnesiumPerPill = data["UnitsMagnesiumPerPill"] # shape: [], definition: Units of magnesium per pill

UnitsZincPerPill = data["UnitsZincPerPill"] # shape: [], definition: Units of zinc per pill

MinimumNumberOfPills = data["MinimumNumberOfPills"] # shape: [], definition: Minimum number of pills

MinimumGummiesToPillsRatio = data["MinimumGummiesToPillsRatio"] # shape: [], definition: Minimum gummies to pills ratio

MaximumUnitsOfMagnesium = data["MaximumUnitsOfMagnesium"] # shape: [], definition: Maximum units of magnesium consumption



### Define the variables

NumberOfGummies = model.addVar(vtype=GRB.INTEGER, name="NumberOfGummies")

NumberOfPills = model.addVar(vtype=GRB.INTEGER, name="NumberOfPills")



### Define the constraints

model.addConstr(UnitsMagnesiumPerGummy * NumberOfGummies + UnitsMagnesiumPerPill * NumberOfPills <= MaximumUnitsOfMagnesium)
model.addConstr(NumberOfPills >= MinimumNumberOfPills)
model.addConstr(NumberOfGummies >= MinimumGummiesToPillsRatio * NumberOfPills)


### Define the objective

del.setObjective(UnitsZincPerGummy * NumberOfGummies + UnitsZincPerPill * NumberOfPills, GRB.MAXIMIZE


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
