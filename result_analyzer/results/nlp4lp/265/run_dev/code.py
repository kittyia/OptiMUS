
import os
import numpy as np
import json 
from gurobipy import Model, GRB, quicksum


model = Model("OptimizationProblem")

with open("data.json", "r") as f:
    data = json.load(f)




### Define the parameters

TimeChemicalA = data["TimeChemicalA"] # shape: [], definition: Time for one unit of chemical A to become effective

TimeChemicalB = data["TimeChemicalB"] # shape: [], definition: Time for one unit of chemical B to become effective

MaxRatioAtoB = data["MaxRatioAtoB"] # shape: [], definition: Maximum ratio of chemical A to chemical B

MinChemicalA = data["MinChemicalA"] # shape: [], definition: Minimum units of chemical A required

MinTotalChemicals = data["MinTotalChemicals"] # shape: [], definition: Minimum total units of chemicals in the mixer



### Define the variables

ChemicalAUnits = model.addVar(vtype=GRB.INTEGER, name="ChemicalAUnits")

ChemicalBUnits = model.addVar(vtype=GRB.INTEGER, name="ChemicalBUnits")



### Define the constraints

model.addConstr(ChemicalAUnits >= MinChemicalA)
model.addConstr(ChemicalAUnits + ChemicalBUnits >= MinTotalChemicals)
model.addConstr(ChemicalAUnits <= MaxRatioAtoB * ChemicalBUnits)


### Define the objective

model.setObjective(TimeChemicalA * ChemicalAUnits + TimeChemicalB * ChemicalBUnits, GRB.MINIMIZE)


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
