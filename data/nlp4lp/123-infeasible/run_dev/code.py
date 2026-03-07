
import os
import numpy as np
import json 
from gurobipy import Model, GRB, quicksum


model = Model("OptimizationProblem")

with open("data.json", "r") as f:
    data = json.load(f)




### Define the parameters

TotalPainkillerUnits = data["TotalPainkillerUnits"] # shape: [], definition: TotalPainkillerUnits

PainkillerPerDayPill = data["PainkillerPerDayPill"] # shape: [], definition: PainkillerPerDayPill

SleepPerDayPill = data["SleepPerDayPill"] # shape: [], definition: SleepPerDayPill

PainkillerPerNightPill = data["PainkillerPerNightPill"] # shape: [], definition: PainkillerPerNightPill

SleepPerNightPill = data["SleepPerNightPill"] # shape: [], definition: SleepPerNightPill

MinDayPillPercentage = data["MinDayPillPercentage"] # shape: [], definition: MinDayPillPercentage

MinNightPills = data["MinNightPills"] # shape: [], definition: MinNightPills



### Define the variables

DayPills = model.addVar(vtype=GRB.INTEGER, name="DayPills")

NightPills = model.addVar(vtype=GRB.INTEGER, name="NightPills")



### Define the constraints

model.addConstr(PainkillerPerDayPill * DayPills + PainkillerPerNightPill * NightPills <= TotalPainkillerUnits)
model.addConstr(DayPills >= MinDayPillPercentage * (DayPills + NightPills))
model.addConstr(NightPills >= MinNightPills)


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
