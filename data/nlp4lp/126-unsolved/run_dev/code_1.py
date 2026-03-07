import os
import numpy as np
import json
from gurobipy import Model, GRB, quicksum


model = Model("OptimizationProblem")

with open("data.json", "r") as f:
    data = json.load(f)


### Define the parameters

NumLabs = data["NumLabs"]
NumPillTypes = data["NumPillTypes"]
ProductionRate = data["ProductionRate"]
WorkerLaborPerLab = data["WorkerLaborPerLab"]
TotalWorkerHours = data["TotalWorkerHours"]
MinRequiredPills = data["MinRequiredPills"]


### Define the variables

HoursRun = model.addVars(NumLabs, vtype=GRB.CONTINUOUS, name="HoursRun")


### Define the constraints

# Worker hour constraint
model.addConstr(
    quicksum(WorkerLaborPerLab[i] * HoursRun[i] for i in range(NumLabs))
    <= TotalWorkerHours
)

# Production constraints
for p in range(NumPillTypes):
    model.addConstr(
        quicksum(ProductionRate[i][p] * HoursRun[i] for i in range(NumLabs))
        >= MinRequiredPills[p]
    )

# Non-negativity (redundant but explicit)
for i in range(NumLabs):
    model.addConstr(HoursRun[i] >= 0)


### Define the objective

model.setObjective(
    quicksum(HoursRun[l] for l in range(NumLabs)),
    GRB.MINIMIZE
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