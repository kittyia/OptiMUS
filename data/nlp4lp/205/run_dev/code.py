
import os
import numpy as np
import json 
from gurobipy import Model, GRB, quicksum


model = Model("OptimizationProblem")

with open("data.json", "r") as f:
    data = json.load(f)




### Define the parameters

InspectionTimeWashingMachine = data["InspectionTimeWashingMachine"] # shape: [], definition: Time required to inspect one washing machine

FixingTimeWashingMachine = data["FixingTimeWashingMachine"] # shape: [], definition: Time required to fix one washing machine

InspectionTimeFreezer = data["InspectionTimeFreezer"] # shape: [], definition: Time required to inspect one freezer

FixingTimeFreezer = data["FixingTimeFreezer"] # shape: [], definition: Time required to fix one freezer

TotalInspectionTime = data["TotalInspectionTime"] # shape: [], definition: Total available time for inspections

TotalScheduleTime = data["TotalScheduleTime"] # shape: [], definition: Total available schedule time

EarningsPerWashingMachine = data["EarningsPerWashingMachine"] # shape: [], definition: Earnings per washing machine repaired

EarningsPerFreezer = data["EarningsPerFreezer"] # shape: [], definition: Earnings per freezer repaired



### Define the variables

NumberWashingMachines = model.addVar(vtype=GRB.INTEGER, name="NumberWashingMachines")

NumberFreezers = model.addVar(vtype=GRB.INTEGER, name="NumberFreezers")



### Define the constraints

model.addConstr(
    InspectionTimeWashingMachine * NumberWashingMachines
    + InspectionTimeFreezer * NumberFreezers
    <= TotalInspectionTime
)
model.addConstr(FixingTimeWashingMachine * NumberWashingMachines + FixingTimeFreezer * NumberFreezers <= TotalScheduleTime)
model.addConstr(NumberWashingMachines >= 0)
model.addConstr(NumberFreezers >= 0)


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
