
import os
import numpy as np
import json 
from gurobipy import Model, GRB, quicksum


model = Model("OptimizationProblem")

with open("data.json", "r") as f:
    data = json.load(f)




### Define the parameters

TotalAcres = data["TotalAcres"] # shape: [], definition: Total available acres for growing

MinApplesAcres = data["MinApplesAcres"] # shape: [], definition: Minimum acres allocated to apples

MinPearsAcres = data["MinPearsAcres"] # shape: [], definition: Minimum acres allocated to pears

ProfitPerAcreApples = data["ProfitPerAcreApples"] # shape: [], definition: Profit per acre of apples

ProfitPerAcrePears = data["ProfitPerAcrePears"] # shape: [], definition: Profit per acre of pears

MaxPearsToApplesRatio = data["MaxPearsToApplesRatio"] # shape: [], definition: Maximum ratio of pear acreage to apple acreage



### Define the variables

AcresApples = model.addVar(vtype=GRB.CONTINUOUS, name="AcresApples")

AcresPears = model.addVar(vtype=GRB.CONTINUOUS, name="AcresPears")



### Define the constraints

model.addConstr(AcresApples >= MinApplesAcres)
model.addConstr(AcresPears >= MinPearsAcres)
model.addConstr(AcresApples + AcresPears <= TotalAcres)
model.addConstr(AcresPears <= MaxPearsToApplesRatio * AcresApples)


### Define the objective

model.setObjective(
    ProfitPerAcreApples * AcresApples + ProfitPerAcrePears * AcresPears,
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
