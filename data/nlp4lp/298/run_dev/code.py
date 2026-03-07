
import os
import numpy as np
import json 
from gurobipy import Model, GRB, quicksum


model = Model("OptimizationProblem")

with open("data.json", "r") as f:
    data = json.load(f)




### Define the parameters

MaxWideTrails = data["MaxWideTrails"] # shape: [], definition: Maximum number of wide trails allowed

MaxVisitorsPerDay = data["MaxVisitorsPerDay"] # shape: [], definition: Maximum number of visitors allowed per day

VisitorsPerWideTrail = data["VisitorsPerWideTrail"] # shape: [], definition: Number of visitors per day on a wide trail

VisitorsPerNarrowTrail = data["VisitorsPerNarrowTrail"] # shape: [], definition: Number of visitors per day on a narrow trail

GarbagePerWideTrail = data["GarbagePerWideTrail"] # shape: [], definition: Units of garbage produced per wide trail

GarbagePerNarrowTrail = data["GarbagePerNarrowTrail"] # shape: [], definition: Units of garbage produced per narrow trail



### Define the variables

numWideTrails = model.addVar(vtype=GRB.INTEGER, name="numWideTrails")

numNarrowTrails = model.addVar(vtype=GRB.INTEGER, name="numNarrowTrails")



### Define the constraints

model.addConstr(numWideTrails <= MaxWideTrails)
model.addConstr(VisitorsPerWideTrail * numWideTrails + VisitorsPerNarrowTrail * numNarrowTrails <= MaxVisitorsPerDay)
model.addConstr(numWideTrails >= 0)
model.addConstr(numNarrowTrails >= 0)


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
