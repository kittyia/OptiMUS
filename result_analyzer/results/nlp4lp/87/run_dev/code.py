
import os
import numpy as np
import json 
from gurobipy import Model, GRB, quicksum


model = Model("OptimizationProblem")

with open("data.json", "r") as f:
    data = json.load(f)




### Define the parameters

NumPrinterTypes = data["NumPrinterTypes"] # shape: [], definition: Number of different printer types

PrintingSpeed = data["PrintingSpeed"] # shape: ['NumPrinterTypes'], definition: Pages printed per minute by each printer type

InkUsage = data["InkUsage"] # shape: ['NumPrinterTypes'], definition: Ink units used per minute by each printer type

MinPagesPerMinute = data["MinPagesPerMinute"] # shape: [], definition: Minimum number of pages to be printed per minute

MaxInkPerMinute = data["MaxInkPerMinute"] # shape: [], definition: Maximum number of ink units allowed per minute



### Define the variables

NumPrinters = model.addVars(NumPrinterTypes, vtype=GRB.INTEGER, name="NumPrinters")



### Define the constraints

model.addConstr(
    sum(PrintingSpeed[t] * NumPrinters[t] for t in range(NumPrinterTypes)) 
    >= MinPagesPerMinute
)
model.addConstr(
    sum(InkUsage[i] * NumPrinters[i] for i in range(NumPrinterTypes)) 
    <= MaxInkPerMinute
)
model.addConstr(NumPrinters[1] <= NumPrinters[0] - 1)
for i in range(NumPrinterTypes):
    model.addConstr(NumPrinters[i] >= 0)


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
