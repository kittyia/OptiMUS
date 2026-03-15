
import os
import numpy as np
import json 
from gurobipy import Model, GRB, quicksum


model = Model("OptimizationProblem")

with open("data.json", "r") as f:
    data = json.load(f)




### Define the parameters

TotalLand = data["TotalLand"] # shape: [], definition: Total land available for mining in square miles

TotalMachines = data["TotalMachines"] # shape: [], definition: Total number of extraction machines available

MaxWastewater = data["MaxWastewater"] # shape: [], definition: Maximum allowed polluted wastewater per day in tons

NumTechniques = data["NumTechniques"] # shape: [], definition: Number of mining techniques

ProductionRate = data["ProductionRate"] # shape: ['NumTechniques'], definition: Daily production of rare earth oxide per square mile for each mining technique

WastewaterRate = data["WastewaterRate"] # shape: ['NumTechniques'], definition: Daily polluted wastewater created per square mile for each mining technique

MachinesRequired = data["MachinesRequired"] # shape: ['NumTechniques'], definition: Number of extraction machines required per square mile for each mining technique



### Define the variables

LandUsed = model.addVars(NumTechniques, vtype=GRB.CONTINUOUS, name="LandUsed")



### Define the constraints

model.addConstr(
    sum(MachinesRequired[t] * LandUsed[t] for t in range(NumTechniques)) 
    <= TotalMachines
)
model.addConstr(
    sum(WastewaterRate[t] * LandUsed[t] for t in range(NumTechniques)) 
    <= MaxWastewater
)
for t in range(NumTechniques):
    model.addConstr(LandUsed[t] >= 0)


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
