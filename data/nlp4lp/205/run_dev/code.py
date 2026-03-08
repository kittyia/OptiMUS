
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

WashingMachinesRepaired = model.addVar(vtype=GRB.INTEGER, name="WashingMachinesRepaired")

FreezersRepaired = model.addVar(vtype=GRB.INTEGER, name="FreezersRepaired")



### Define the constraints

model.addConstr(InspectionTimeWashingMachine * WashingMachinesRepaired + InspectionTimeFreezer * FreezersRepaired <= TotalInspectionTime)
model.addConstr(
    FixingTimeWashingMachine * WashingMachinesRepaired
    + FixingTimeFreezer * FreezersRepaired
    <= TotalScheduleTime
)
model.addConstr(WashingMachinesRepaired >= 0)
model.addConstr(FreezersRepaired >= 0)
model.addConstr(WashingMachinesRepaired >= 0)
model.addConstr(FreezersRepaired >= 0)


### Define the objective

model.setObjective(EarningsPerWashingMachine * WashingMachinesRepaired + EarningsPerFreezer * FreezersRepaired, GRB.MAXIMIZE)


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
