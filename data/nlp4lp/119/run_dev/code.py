
import os
import numpy as np
import json 
from gurobipy import Model, GRB, quicksum


model = Model("OptimizationProblem")

with open("data.json", "r") as f:
    data = json.load(f)




### Define the parameters

TimeThroatSwab = data["TimeThroatSwab"] # shape: [], definition: Time required to perform one throat swab in minutes

TimeNasalSwab = data["TimeNasalSwab"] # shape: [], definition: Time required to perform one nasal swab in minutes

MinimumNasalSwabs = data["MinimumNasalSwabs"] # shape: [], definition: Minimum number of nasal swabs to be performed

ThroatToNasalRatio = data["ThroatToNasalRatio"] # shape: [], definition: Minimum ratio of throat swabs to nasal swabs

TotalOperationalTime = data["TotalOperationalTime"] # shape: [], definition: Total operational time available in minutes



### Define the variables

ThroatSwabs = model.addVar(vtype=GRB.INTEGER, name="ThroatSwabs")

NasalSwabs = model.addVar(vtype=GRB.INTEGER, name="NasalSwabs")



### Define the constraints

model.addConstr(TimeThroatSwab * ThroatSwabs + TimeNasalSwab * NasalSwabs <= TotalOperationalTime)
model.addConstr(NasalSwabs >= MinimumNasalSwabs)
model.addConstr(ThroatSwabs >= ThroatToNasalRatio * NasalSwabs)


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
