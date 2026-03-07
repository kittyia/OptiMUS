import os
import numpy as np
import json
from gurobipy import Model, GRB, quicksum


model = Model("OptimizationProblem")

with open("data.json", "r") as f:
    data = json.load(f)

### Define the parameters

NumProcesses = data["NumProcesses"]
NumProducts = data["NumProducts"]
ProductionRate = data["ProductionRate"]
PreliminaryMaterialRequired = data["PreliminaryMaterialRequired"]
TotalPreliminaryMaterialAvailable = data["TotalPreliminaryMaterialAvailable"]
MinProductRequired = data["MinProductRequired"]

### Define the variables

ProcessTime = model.addVars(NumProcesses, vtype=GRB.CONTINUOUS, name="ProcessTime")

### Define the constraints

# Preliminary material constraint
model.addConstr(
    quicksum(PreliminaryMaterialRequired[p] * ProcessTime[p] for p in range(NumProcesses))
    <= TotalPreliminaryMaterialAvailable
)

# Product requirements
for prod in range(NumProducts):
    model.addConstr(
        quicksum(ProductionRate[p][prod] * ProcessTime[p] for p in range(NumProcesses))
        >= MinProductRequired[prod]
    )

# Non-negativity (already ensured by default, but kept for clarity)
for p in range(NumProcesses):
    model.addConstr(ProcessTime[p] >= 0)

### Define the objective

model.setObjective(quicksum(ProcessTime[p] for p in range(NumProcesses)), GRB.MINIMIZE)

### Optimize the model

model.optimize()

### Output optimal objective value

if model.status == GRB.OPTIMAL:
    print("Optimal Objective Value: ", model.ObjVal)
    with open("output_solution.txt", "w") as f:
        f.write(str(model.ObjVal))
else:
    with open("output_solution.txt", "w") as f:
        f.write(str(model.status))