
import os
import numpy as np
import json 
from gurobipy import Model, GRB, quicksum


model = Model("OptimizationProblem")

with open("data.json", "r") as f:
    data = json.load(f)




### Define the parameters

CashMachineProcessingRate = data["CashMachineProcessingRate"] # shape: [], definition: Processing rate of a cash-based machine in people per hour

CardMachineProcessingRate = data["CardMachineProcessingRate"] # shape: [], definition: Processing rate of a card-only machine in people per hour

CashMachinePaperRolls = data["CashMachinePaperRolls"] # shape: [], definition: Number of paper rolls used per hour by a cash-based machine

CardMachinePaperRolls = data["CardMachinePaperRolls"] # shape: [], definition: Number of paper rolls used per hour by a card-only machine

MinPeopleProcessed = data["MinPeopleProcessed"] # shape: [], definition: Minimum number of people that must be processed per hour

MaxPaperRolls = data["MaxPaperRolls"] # shape: [], definition: Maximum number of paper rolls that can be used per hour



### Define the variables

CashMachines = model.addVar(vtype=GRB.INTEGER, name="CashMachines")

CardMachines = model.addVar(vtype=GRB.INTEGER, name="CardMachines")



### Define the constraints

model.addConstr(CashMachineProcessingRate * CashMachines + CardMachineProcessingRate * CardMachines >= MinPeopleProcessed)
model.addConstr(CashMachinePaperRolls * CashMachines + CardMachinePaperRolls * CardMachines <= MaxPaperRolls)
model.addConstr(CardMachines <= CashMachines)
model.addConstr(CashMachines >= 0)
model.addConstr(CardMachines >= 0)


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
