
import os
import numpy as np
import json 
from gurobipy import Model, GRB, quicksum


model = Model("OptimizationProblem")

with open("data.json", "r") as f:
    data = json.load(f)




### Define the parameters

UltrasoundTechnicianShiftHours = data["UltrasoundTechnicianShiftHours"] # shape: [], definition: The number of hours an ultrasound technician works per shift

GraduateResearcherShiftHours = data["GraduateResearcherShiftHours"] # shape: [], definition: The number of hours a graduate researcher works per shift

UltrasoundTechnicianPayment = data["UltrasoundTechnicianPayment"] # shape: [], definition: The payment an ultrasound technician receives per shift

GraduateResearcherPayment = data["GraduateResearcherPayment"] # shape: [], definition: The payment a graduate researcher receives per shift

ShiftRatio = data["ShiftRatio"] # shape: [], definition: The required ratio of ultrasound technician shifts to graduate researcher shifts

RequiredUltrasoundServiceHours = data["RequiredUltrasoundServiceHours"] # shape: [], definition: The total number of ultrasound service hours required

TotalBudget = data["TotalBudget"] # shape: [], definition: The total budget available for workers' payments



### Define the variables

UltrasoundTechnicianShifts = model.addVar(vtype=GRB.INTEGER, name="UltrasoundTechnicianShifts")

GraduateResearcherShifts = model.addVar(vtype=GRB.INTEGER, name="GraduateResearcherShifts")



### Define the constraints

model.addConstr(
    UltrasoundTechnicianShiftHours * UltrasoundTechnicianShifts
    + GraduateResearcherShiftHours * GraduateResearcherShifts
    >= RequiredUltrasoundServiceHours
)
model.addConstr(
    UltrasoundTechnicianPayment * UltrasoundTechnicianShifts
    + GraduateResearcherPayment * GraduateResearcherShifts
    <= TotalBudget
)
model.addConstr(UltrasoundTechnicianShifts == ShiftRatio * GraduateResearcherShifts)
model.addConstr(UltrasoundTechnicianShifts >= 0)
model.addConstr(GraduateResearcherShifts >= 0)
model.addConstr(UltrasoundTechnicianShifts >= 0)
model.addConstr(GraduateResearcherShifts >= 0)


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
