import os
import numpy as np
import json 
from gurobipy import Model, GRB, quicksum


model = Model("OptimizationProblem")

with open("data.json", "r") as f:
    data = json.load(f)


### Define the parameters

UltrasoundTechnicianShiftHours = data["UltrasoundTechnicianShiftHours"]
GraduateResearcherShiftHours = data["GraduateResearcherShiftHours"]

UltrasoundTechnicianPayment = data["UltrasoundTechnicianPayment"]
GraduateResearcherPayment = data["GraduateResearcherPayment"]

ShiftRatio = data["ShiftRatio"]
RequiredUltrasoundServiceHours = data["RequiredUltrasoundServiceHours"]
TotalBudget = data["TotalBudget"]


### Define the variables

UltrasoundTechnicianShifts = model.addVar(vtype=GRB.INTEGER, lb=0, name="UltrasoundTechnicianShifts")
GraduateResearcherShifts = model.addVar(vtype=GRB.INTEGER, lb=0, name="GraduateResearcherShifts")


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

model.addConstr(
    UltrasoundTechnicianShifts == ShiftRatio * GraduateResearcherShifts
)


### Define the objective

model.setObjective(
    UltrasoundTechnicianShifts + GraduateResearcherShifts,
    GRB.MINIMIZE
)


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
``