
import os
import numpy as np
import json 
from gurobipy import Model, GRB, quicksum


model = Model("OptimizationProblem")

with open("data.json", "r") as f:
    data = json.load(f)




### Define the parameters

NumPainKillers = data["NumPainKillers"] # shape: [], definition: Number of different pain killers available

NumTargets = data["NumTargets"] # shape: [], definition: Number of different medicine targets

MedicinePerDose = data["MedicinePerDose"] # shape: ['NumPainKillers', 'NumTargets'], definition: Amount of medicine delivered to each target per dose for each pain killer

MaxSleepMedicine = data["MaxSleepMedicine"] # shape: [], definition: Maximum units of sleeping medicine that can be delivered

MinLegsMedicine = data["MinLegsMedicine"] # shape: [], definition: Minimum units of medicine required for legs



### Define the variables

Doses = model.addVars(NumPainKillers, vtype=GRB.CONTINUOUS, name="Doses")



### Define the constraints

model.addConstr(0.3 * Doses[0] + 0.6 * Doses[1] <= MaxSleepMedicine)
model.addConstr(
    sum(MedicinePerDose[i][0] * Doses[i] for i in range(NumPainKillers)) 
    >= MinLegsMedicine
)
for i in range(NumPainKillers):
    model.addConstr(Doses[i] >= 0)


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
