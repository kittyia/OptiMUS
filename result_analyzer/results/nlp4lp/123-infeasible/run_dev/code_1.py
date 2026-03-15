import os
import numpy as np
import json
from gurobipy import Model, GRB, quicksum

model = Model("OptimizationProblem")

with open("data.json", "r") as f:
    data = json.load(f)

### Define the parameters

TotalPainkillerUnits = data["TotalPainkillerUnits"]
PainkillerPerDayPill = data["PainkillerPerDayPill"]
SleepPerDayPill = data["SleepPerDayPill"]
PainkillerPerNightPill = data["PainkillerPerNightPill"]
SleepPerNightPill = data["SleepPerNightPill"]
MinDayPillPercentage = data["MinDayPillPercentage"]
MinNightPills = data["MinNightPills"]

### Define the variables

DayPills = model.addVar(vtype=GRB.INTEGER, name="DayPills")
NightPills = model.addVar(vtype=GRB.INTEGER, name="NightPills")

### Define the constraints

model.addConstr(
    PainkillerPerDayPill * DayPills +
    PainkillerPerNightPill * NightPills
    <= TotalPainkillerUnits
)

model.addConstr(
    DayPills >= MinDayPillPercentage * (DayPills + NightPills)
)

model.addConstr(
    NightPills >= MinNightPills
)

### Define the objective

model.setObjective(
    SleepPerDayPill * DayPills +
    SleepPerNightPill * NightPills,
    GRB.MINIMIZE
)

### Optimize the model

model.optimize()

### Output optimal objective value

if model.Status == GRB.OPTIMAL:
    print("Optimal Objective Value: ", model.ObjVal)
    with open("output_solution.txt", "w") as f:
        f.write(str(model.ObjVal))
else:
    with open("output_solution.txt", "w") as f:
        f.write(str(model.Status))