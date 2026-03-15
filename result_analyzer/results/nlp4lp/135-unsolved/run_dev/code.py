
import os
import numpy as np
import json 
from gurobipy import Model, GRB, quicksum


model = Model("OptimizationProblem")

with open("data.json", "r") as f:
    data = json.load(f)




### Define the parameters

NumProcesses = data["NumProcesses"] # shape: [], definition: NumProcesses

NumProducts = data["NumProducts"] # shape: [], definition: NumProducts

ProductionRate = data["ProductionRate"] # shape: [2, 2], definition: ProductionRate

PreliminaryMaterialRequired = data["PreliminaryMaterialRequired"] # shape: [2], definition: PreliminaryMaterialRequired

TotalPreliminaryMaterialAvailable = data["TotalPreliminaryMaterialAvailable"] # shape: [], definition: TotalPreliminaryMaterialAvailable

MinProductRequired = data["MinProductRequired"] # shape: [2], definition: MinProductRequired



### Define the variables

HoursProcess = model.addVars(NumProcesses, vtype=GRB.CONTINUOUS, name="HoursProcess")



### Define the constraints

model.addConstr(
    sum(PreliminaryMaterialRequired[i] * HoursProcess[i] for i in range(NumProcesses))
    <= TotalPreliminaryMaterialAvailable
)
model.addConstr(35 * HoursProcess[0] + 50 * HoursProcess[1] >= 1200)
model.addConstr(12 * HoursProcess[0] + 30 * HoursProcess[1] >= 1200)
model.addConstr(HoursProcess[0] >= 0)
model.addConstr(HoursProcess[1] >= 0)


### Define the objective

model.setObjective(quicksum(HoursProcess[p] for p in range(NumProcesses)), GRB.MINIMIZE)


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
