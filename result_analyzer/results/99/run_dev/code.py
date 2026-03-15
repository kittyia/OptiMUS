
import os
import numpy as np
import json 
from gurobipy import Model, GRB, quicksum


model = Model("OptimizationProblem")

with open("data.json", "r") as f:
    data = json.load(f)




### Define the parameters

AutomaticMachineTimePerPatient = data["AutomaticMachineTimePerPatient"] # shape: [], definition: Time taken by the automatic machine to process one patient.

ManualMachineTimePerPatient = data["ManualMachineTimePerPatient"] # shape: [], definition: Time taken by the manual machine to process one patient.

ManualPatientMinRatio = data["ManualPatientMinRatio"] # shape: [], definition: Minimum ratio of manual machine patients to automatic machine patients.

AutomaticMachineMinimumPatients = data["AutomaticMachineMinimumPatients"] # shape: [], definition: Minimum number of patients that must be processed by the automatic machine.

TotalAvailableTime = data["TotalAvailableTime"] # shape: [], definition: Total available time for the clinic in minutes.



### Define the variables

AutomaticPatients = model.addVar(vtype=GRB.INTEGER, name="AutomaticPatients")

ManualPatients = model.addVar(vtype=GRB.INTEGER, name="ManualPatients")



### Define the constraints

model.addConstr(
    AutomaticMachineTimePerPatient * AutomaticPatients
    + ManualMachineTimePerPatient * ManualPatients
    <= TotalAvailableTime
)
model.addConstr(ManualPatients >= ManualPatientMinRatio * AutomaticPatients)
model.addConstr(AutomaticPatients >= AutomaticMachineMinimumPatients)


### Define the objective

model.setObjective(AutomaticPatients + ManualPatients, GRB.MAXIMIZE)


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
