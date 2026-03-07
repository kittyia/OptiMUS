
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

NumColorPrinters = model.addVar(vtype=GRB.INTEGER, name="NumColorPrinters")

NumBWPrinters = model.addVar(vtype=GRB.INTEGER, name="NumBWPrinters")



### Define the constraints

model.addConstr(NumColorPrinters <= MaxColorPrinters))
model.addConstr(NumBWPrinters <= MaxBWPrinters)
model.addConstr(NumColorPrinters + NumBWPrinters <= MaxMachineCapacity)
model.addConstr(NumColorPrinters >= 0)
model.addConstr(NumBWPrinters >= 0)


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
