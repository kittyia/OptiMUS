
import os
import numpy as np
import json 
from gurobipy import Model, GRB, quicksum


model = Model("OptimizationProblem")

with open("data.json", "r") as f:
    data = json.load(f)




### Define the parameters

NumDemonstrations = data["NumDemonstrations"] # shape: [], definition: Number of demonstrations

MintUsed = data["MintUsed"] # shape: ['NumDemonstrations'], definition: Amount of mint used by each demonstration

ActiveIngredientUsed = data["ActiveIngredientUsed"] # shape: ['NumDemonstrations'], definition: Amount of active ingredient used by each demonstration

FoamProduced = data["FoamProduced"] # shape: ['NumDemonstrations'], definition: Amount of minty foam produced by each demonstration

BlackTarProduced = data["BlackTarProduced"] # shape: ['NumDemonstrations'], definition: Amount of black tar produced by each demonstration

TotalMintAvailable = data["TotalMintAvailable"] # shape: [], definition: Total units of mint available

TotalActiveIngredientAvailable = data["TotalActiveIngredientAvailable"] # shape: [], definition: Total units of active ingredient available

MaxBlackTarAllowed = data["MaxBlackTarAllowed"] # shape: [], definition: Maximum units of black tar allowed



### Define the variables

NumDemos = model.addVars(NumDemonstrations, vtype=GRB.INTEGER, name="NumDemos")



### Define the constraints

model.addConstr(sum(ActiveIngredientUsed[i] * NumDemos[i] for i in range(NumDemonstrations)) <= TotalActiveIngredientAvailable)
model.addConstr(NumDemos[0] >= 0)
model.addConstr(NumDemos[1] >= 0)


### Define the objective

model.setObjective(quicksum(FoamProduced[i] * NumDemos[i] for i in range(NumDemonstrations)), GRB.MAXIMIZE)


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
