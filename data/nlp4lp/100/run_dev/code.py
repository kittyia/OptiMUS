
import os
import numpy as np
import json 
from gurobipy import Model, GRB, quicksum


model = Model("OptimizationProblem")

with open("data.json", "r") as f:
    data = json.load(f)




### Define the parameters

NumSyrups = data["NumSyrups"] # shape: [], definition: Number of available syrups

MedicineThroatPerServing = data["MedicineThroatPerServing"] # shape: ['NumSyrups'], definition: Amount of medicine delivered to the throat per serving of each syrup

MedicineLungsPerServing = data["MedicineLungsPerServing"] # shape: ['NumSyrups'], definition: Amount of medicine delivered to the lungs per serving of each syrup

SugarPerServing = data["SugarPerServing"] # shape: ['NumSyrups'], definition: Amount of sugar per serving of each syrup

MaxMedicineThroat = data["MaxMedicineThroat"] # shape: [], definition: Maximum total medicine allowed for the throat

MinMedicineLungs = data["MinMedicineLungs"] # shape: [], definition: Minimum total medicine required for the lungs



### Define the variables

Servings = model.addVars(NumSyrups, vtype=GRB.CONTINUOUS, name="Servings")



### Define the constraints

model.addConstr(
    sum(MedicineThroatPerServing[s] * Servings[s] for s in range(NumSyrups))
    <= MaxMedicineThroat
)
model.addConstr(
    sum(MedicineLungsPerServing[i] * Servings[i] for i in range(NumSyrups))
    >= MinMedicineLungs
)
for i in range(NumSyrups):
    model.addConstr(Servings[i] >= 0)


### Define the objective

model.setObjective(quicksum(SugarPerServing[i] * Servings[i] for i in range(NumSyrups)), GRB.MINIMIZE)


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
