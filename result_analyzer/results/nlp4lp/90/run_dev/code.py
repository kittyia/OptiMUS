
import os
import numpy as np
import json 
from gurobipy import Model, GRB, quicksum


model = Model("OptimizationProblem")

with open("data.json", "r") as f:
    data = json.load(f)




### Define the parameters

NumPillTypes = data["NumPillTypes"] # shape: [], definition: Number of pill types

PainMedicationPerPill = data["PainMedicationPerPill"] # shape: ['NumPillTypes'], definition: Amount of pain medication provided by one unit of each pill type

AnxietyMedicationPerPill = data["AnxietyMedicationPerPill"] # shape: ['NumPillTypes'], definition: Amount of anxiety medication provided by one unit of each pill type

DischargePerPill = data["DischargePerPill"] # shape: ['NumPillTypes'], definition: Amount of discharge caused by one unit of each pill type

MaxPainMedication = data["MaxPainMedication"] # shape: [], definition: Maximum units of pain medication allowed

MinAnxietyMedication = data["MinAnxietyMedication"] # shape: [], definition: Minimum units of anxiety medication required



### Define the variables

NumPills = model.addVars(NumPillTypes, vtype=GRB.INTEGER, name="NumPills")



### Define the constraints

model.addConstr(
    sum(PainMedicationPerPill[i] * NumPills[i] for i in range(NumPillTypes))
    <= MaxPainMedication
)
model.addConstr(
    sum(AnxietyMedicationPerPill[i] * NumPills[i] for i in range(NumPillTypes)) 
    >= MinAnxietyMedication
)
for i in range(NumPillTypes):
    model.addConstr(NumPills[i] >= 0)


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
