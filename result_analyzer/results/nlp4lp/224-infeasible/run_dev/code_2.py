import json
from gurobipy import Model, GRB

# Create model
model = Model("OptimizationProblem")

# Load data
with open("data.json", "r") as f:
    data = json.load(f)

# Define parameters
UltrasoundTechnicianShiftHours = data["UltrasoundTechnicianShiftHours"]
GraduateResearcherShiftHours = data["GraduateResearcherShiftHours"]

UltrasoundTechnicianPayment = data["UltrasoundTechnicianPayment"]
GraduateResearcherPayment = data["GraduateResearcherPayment"]

ShiftRatio = data["ShiftRatio"]
RequiredUltrasoundServiceHours = data["RequiredUltrasoundServiceHours"]
TotalBudget = data["TotalBudget"]

# Define decision variables
UltrasoundTechnicianShifts = model.addVar(
    vtype=GRB.INTEGER, lb=0, name="UltrasoundTechnicianShifts"
)
GraduateResearcherShifts = model.addVar(
    vtype=GRB.INTEGER, lb=0, name="GraduateResearcherShifts"
)

# Add constraints
model.addConstr(
    UltrasoundTechnicianShiftHours * UltrasoundTechnicianShifts
    + GraduateResearcherShiftHours * GraduateResearcherShifts
    >= RequiredUltrasoundServiceHours,
    name="ServiceHoursRequirement"
)

model.addConstr(
    UltrasoundTechnicianPayment * UltrasoundTechnicianShifts
    + GraduateResearcherPayment * GraduateResearcherShifts
    <= TotalBudget,
    name="BudgetConstraint"
)

model.addConstr(
    UltrasoundTechnicianShifts == ShiftRatio * GraduateResearcherShifts,
    name="ShiftRatioConstraint"
)

# Set objective: minimize total number of workers
model.setObjective(
    UltrasoundTechnicianShifts + GraduateResearcherShifts,
    GRB.MINIMIZE
)

# Optimize model
model.optimize()

# Output optimal objective value
if model.status == GRB.OPTIMAL:
    print("Optimal Objective Value:", model.ObjVal)
    with open("output_solution.txt", "w") as f:
        f.write(str(model.ObjVal))
else:
    with open("output_solution.txt", "w") as f:
        f.write(str(model.status))