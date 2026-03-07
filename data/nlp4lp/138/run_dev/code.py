
import os
import numpy as np
import json 
from gurobipy import Model, GRB, quicksum


model = Model("OptimizationProblem")

with open("data.json", "r") as f:
    data = json.load(f)




### Define the parameters

TimePerPill = data["TimePerPill"] # shape: [], definition: Time required to administer a pill vaccine

TimePerShot = data["TimePerShot"] # shape: [], definition: Time required to administer a shot vaccine

ShotToPillRatio = data["ShotToPillRatio"] # shape: [], definition: Minimum ratio of shots to pills

MinPills = data["MinPills"] # shape: [], definition: Minimum number of pill vaccines to administer

TotalOperatingTime = data["TotalOperatingTime"] # shape: [], definition: Total operating time of the clinic in minutes



### Define the variables

PillVaccines = model.addVar(vtype=GRB.INTEGER, name="PillVaccines")

ShotVaccines = model.addVar(vtype=GRB.INTEGER, name="ShotVaccines")



### Define the constraints

model.addConstr(TimePerPill * PillVaccines + TimePerShot * ShotVaccines <= TotalOperatingTime)
model.addConstr(ShotVaccines >= ShotToPillRatio * PillVaccines)
model.addConstr(PillVaccines >= MinPills)


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
