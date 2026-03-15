
import os
import numpy as np
import json 
from gurobipy import Model, GRB, quicksum


model = Model("OptimizationProblem")

with open("data.json", "r") as f:
    data = json.load(f)




### Define the parameters

NumProcesses = data["NumProcesses"] # shape: [], definition: Number of available processes

WoodRequiredPerProcess = data["WoodRequiredPerProcess"] # shape: ['NumProcesses'], definition: Amount of wood required for each process

OxygenRequiredPerProcess = data["OxygenRequiredPerProcess"] # shape: ['NumProcesses'], definition: Amount of oxygen required for each process

CO2ProducedPerProcess = data["CO2ProducedPerProcess"] # shape: ['NumProcesses'], definition: Amount of carbon dioxide produced by each process

TotalWoodAvailable = data["TotalWoodAvailable"] # shape: [], definition: Total amount of wood available

TotalOxygenAvailable = data["TotalOxygenAvailable"] # shape: [], definition: Total amount of oxygen available



### Define the variables

ProcessUsage = model.addVars(NumProcesses, vtype=GRB.CONTINUOUS, name="ProcessUsage")



### Define the constraints

model.addConstr(
    sum(WoodRequiredPerProcess[i] * ProcessUsage[i] for i in range(NumProcesses))
    <= TotalWoodAvailable
)
model.addConstr(20 * ProcessUsage[0] + 12 * ProcessUsage[1] <= TotalOxygenAvailable)
for i in range(NumProcesses):
    model.addConstr(ProcessUsage[i] >= 0)


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
