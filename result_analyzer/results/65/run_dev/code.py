
import os
import numpy as np
import json 
from gurobipy import Model, GRB, quicksum


model = Model("OptimizationProblem")

with open("data.json", "r") as f:
    data = json.load(f)




### Define the parameters

TotalAcres = data["TotalAcres"] # shape: [], definition: Total available land in acres

TotalFuel = data["TotalFuel"] # shape: [], definition: Total available fuel in liters

MaxWaste = data["MaxWaste"] # shape: [], definition: Maximum allowable waste in kilograms

NumMachineTypes = data["NumMachineTypes"] # shape: [], definition: Number of machine types

PickRate = data["PickRate"] # shape: ['NumMachineTypes'], definition: Amount of tea leaves picked per acre by each machine type

WasteRate = data["WasteRate"] # shape: ['NumMachineTypes'], definition: Amount of waste created per acre by each machine type

FuelRate = data["FuelRate"] # shape: ['NumMachineTypes'], definition: Amount of fuel required per acre by each machine type



### Define the variables

Acres = model.addVars(NumMachineTypes, vtype=GRB.CONTINUOUS, name="Acres")



### Define the constraints

model.addConstr(sum(Acres[m] for m in range(NumMachineTypes)) <= TotalAcres)
model.addConstr(sum(FuelRate[i] * Acres[i] for i in range(NumMachineTypes)) <= TotalFuel)
model.addConstr(
    sum(WasteRate[m] * Acres[m] for m in range(NumMachineTypes)) <= MaxWaste
)
for m in range(NumMachineTypes):
    model.addConstr(Acres[m] >= 0)


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
