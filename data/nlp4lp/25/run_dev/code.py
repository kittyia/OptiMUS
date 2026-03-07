
import os
import numpy as np
import json 
from gurobipy import Model, GRB, quicksum


model = Model("OptimizationProblem")

with open("data.json", "r") as f:
    data = json.load(f)




### Define the parameters

NumPillTypes = data["NumPillTypes"] # shape: [], definition: Number of different pill types

NumMedicineTypes = data["NumMedicineTypes"] # shape: [], definition: Number of different medicine types

AmountPerPill = data["AmountPerPill"] # shape: ['NumMedicineTypes', 'NumPillTypes'], definition: Amount of a medicine type per pill type

PillCost = data["PillCost"] # shape: ['NumPillTypes'], definition: Cost per pill type

RequiredAmount = data["RequiredAmount"] # shape: ['NumMedicineTypes'], definition: Required amount of a medicine type



### Define the variables

NumPills = model.addVars(NumPillTypes, vtype=GRB.CONTINUOUS, name="NumPills")



### Define the constraints

model.addConstr(
    sum(AmountPerPill[0][j] * NumPills[j] for j in range(NumPillTypes)) >= 40
)
model.addConstr(
    sum(AmountPerPill[1][p] * NumPills[p] for p in range(NumPillTypes)) >= 50
)
model.addConstr(NumPills[0] >= 0)
model.addConstr(NumPills[1] >= 0)


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
