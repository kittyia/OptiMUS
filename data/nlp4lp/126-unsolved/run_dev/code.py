
import os
import numpy as np
import json 
from gurobipy import Model, GRB, quicksum


model = Model("OptimizationProblem")

with open("data.json", "r") as f:
    data = json.load(f)




### Define the parameters

NumLabs = data["NumLabs"] # shape: [], definition: NumLabs

NumPillTypes = data["NumPillTypes"] # shape: [], definition: NumPillTypes

ProductionRate = data["ProductionRate"] # shape: [2, 2], definition: ProductionRate

WorkerLaborPerLab = data["WorkerLaborPerLab"] # shape: [2], definition: WorkerLaborPerLab

TotalWorkerHours = data["TotalWorkerHours"] # shape: [], definition: TotalWorkerHours

MinRequiredPills = data["MinRequiredPills"] # shape: [2], definition: MinRequiredPills



### Define the variables

HoursRun = model.addVars(NumLabs, vtype=GRB.CONTINUOUS, name="HoursRun")



### Define the constraints

model.addConstr(sum(WorkerLaborPerLab[i] * HoursRun[i] for i in range(NumLabs)) <= TotalWorkerHours)
model.addConstr(20 * HoursRun[0] + 30 * HoursRun[1] >= 20000)
model.addConstr(30 * HoursRun[0] + 40 * HoursRun[1] >= 30000)
model.addConstr(HoursRun[0] >= 0)
model.addConstr(HoursRun[1] >= 0)


### Define the objective

del.setObjective(quicksum(HoursRun[l] for l in range(NumLabs)), GRB.MINIMIZE


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
