
import os
import numpy as np
import json 
from gurobipy import Model, GRB, quicksum


model = Model("OptimizationProblem")

with open("data.json", "r") as f:
    data = json.load(f)




### Define the parameters

CleansingChemicalTime = data["CleansingChemicalTime"] # shape: [], definition: Time it takes for one unit of cleansing chemical to be effective

OdorRemovingChemicalTime = data["OdorRemovingChemicalTime"] # shape: [], definition: Time it takes for one unit of odor-removing chemical to be effective

MinCleansingUnits = data["MinCleansingUnits"] # shape: [], definition: Minimum number of units of cleansing chemical to be used per house

MaxTotalUnits = data["MaxTotalUnits"] # shape: [], definition: Maximum total number of chemical units used per house

MaxCleansingToOdorRatio = data["MaxCleansingToOdorRatio"] # shape: [], definition: Maximum ratio of cleansing chemical units to odor-removing chemical units



### Define the variables

CleansingUnits = model.addVar(vtype=GRB.CONTINUOUS, name="CleansingUnits")

OdorRemovingUnits = model.addVar(vtype=GRB.CONTINUOUS, name="OdorRemovingUnits")



### Define the constraints

model.addConstr(CleansingUnits >= MinCleansingUnits)
model.addConstr(CleansingUnits <= MaxCleansingToOdorRatio * OdorRemovingUnits)


### Define the objective




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
