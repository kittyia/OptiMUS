
import os
import numpy as np
import json 
from gurobipy import Model, GRB, quicksum


model = Model("OptimizationProblem")

with open("data.json", "r") as f:
    data = json.load(f)




### Define the parameters

MaxColorPrinters = data["MaxColorPrinters"] # shape: [], definition: Maximum number of color printers produced per day

MaxBWPrinters = data["MaxBWPrinters"] # shape: [], definition: Maximum number of black and white printers produced per day

MaxMachineCapacity = data["MaxMachineCapacity"] # shape: [], definition: Maximum capacity of the shared paper tray installing machine per day

ProfitColorPrinter = data["ProfitColorPrinter"] # shape: [], definition: Profit per color printer

ProfitBWPrinter = data["ProfitBWPrinter"] # shape: [], definition: Profit per black and white printer



### Define the variables

colorPrinters = model.addVar(vtype=GRB.INTEGER, name="colorPrinters")

bwPrinters = model.addVar(vtype=GRB.INTEGER, name="bwPrinters")



### Define the constraints

model.addConstr(colorPrinters >= 0)
model.addConstr(colorPrinters <= MaxColorPrinters)
model.addConstr(bwPrinters >= 0)
model.addConstr(bwPrinters <= MaxBWPrinters)
model.addConstr(colorPrinters + bwPrinters <= MaxMachineCapacity)


### Define the objective

model.setObjective(
    ProfitColorPrinter * colorPrinters + ProfitBWPrinter * bwPrinters,
    GRB.MAXIMIZE
)


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
