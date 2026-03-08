
import os
import numpy as np
import json 
from gurobipy import Model, GRB, quicksum


model = Model("OptimizationProblem")

with open("data.json", "r") as f:
    data = json.load(f)




### Define the parameters

HighVolumeCapacity = data["HighVolumeCapacity"] # shape: [], definition: The daily capacity of a high-volume pipe in US gallons

LowVolumeCapacity = data["LowVolumeCapacity"] # shape: [], definition: The daily capacity of a low-volume pipe in US gallons

TechniciansPerHighVolumePipe = data["TechniciansPerHighVolumePipe"] # shape: [], definition: Number of technicians required to monitor each high-volume pipe daily

TechniciansPerLowVolumePipe = data["TechniciansPerLowVolumePipe"] # shape: [], definition: Number of technicians required to monitor each low-volume pipe daily

DailyGasDemand = data["DailyGasDemand"] # shape: [], definition: Minimum daily US gallons of gas that need to be met

TotalTechnicians = data["TotalTechnicians"] # shape: [], definition: Total number of technicians available daily

MaxHighVolumeProportion = data["MaxHighVolumeProportion"] # shape: [], definition: Maximum allowed proportion of high-volume pipes

MinLowVolumePipes = data["MinLowVolumePipes"] # shape: [], definition: Minimum number of low-volume pipes required



### Define the variables

HighVolumePipes = model.addVar(vtype=GRB.INTEGER, name="HighVolumePipes")

LowVolumePipes = model.addVar(vtype=GRB.INTEGER, name="LowVolumePipes")



### Define the constraints

model.addConstr(HighVolumeCapacity * HighVolumePipes + LowVolumeCapacity * LowVolumePipes >= DailyGasDemand)
model.addConstr(TechniciansPerHighVolumePipe * HighVolumePipes + TechniciansPerLowVolumePipe * LowVolumePipes <= TotalTechnicians)
model.addConstr(HighVolumePipes <= MaxHighVolumeProportion * (HighVolumePipes + LowVolumePipes))
model.addConstr(LowVolumePipes >= MinLowVolumePipes)
model.addConstr(HighVolumePipes >= 0)
model.addConstr(HighVolumePipes >= 0)
model.addConstr(LowVolumePipes >= 0)


### Define the objective

model.setObjective(HighVolumePipes + LowVolumePipes, GRB.MINIMIZE)


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
