
import os
import numpy as np
import json 
from gurobipy import Model, GRB, quicksum


model = Model("OptimizationProblem")

with open("data.json", "r") as f:
    data = json.load(f)




### Define the parameters

ChlorineEffectivenessTime = data["ChlorineEffectivenessTime"] # shape: [], definition: The time in minutes for one unit of chlorine to become effective

WaterSoftenerEffectivenessTime = data["WaterSoftenerEffectivenessTime"] # shape: [], definition: The time in minutes for one unit of water softener to become effective

MaxChlorineToWaterSoftenerRatio = data["MaxChlorineToWaterSoftenerRatio"] # shape: [], definition: The maximum allowed ratio of chlorine to water softener in the pool

MinChlorineUnits = data["MinChlorineUnits"] # shape: [], definition: The minimum required units of chlorine to be added to the pool

TotalChemicalUnits = data["TotalChemicalUnits"] # shape: [], definition: The total number of chemical units to be added to the pool



### Define the variables

ChlorineUnits = model.addVar(vtype=GRB.CONTINUOUS, name="ChlorineUnits")

WaterSoftenerUnits = model.addVar(vtype=GRB.CONTINUOUS, name="WaterSoftenerUnits")



### Define the constraints

model.addConstr(ChlorineUnits <= MaxChlorineToWaterSoftenerRatio * WaterSoftenerUnits)
model.addConstr(ChlorineUnits >= MinChlorineUnits)
model.addConstr(ChlorineUnits + WaterSoftenerUnits == TotalChemicalUnits)


### Define the objective

model.setObjective(
    ChlorineEffectivenessTime * ChlorineUnits +
    WaterSoftenerEffectivenessTime * WaterSoftenerUnits,
    GRB.MINIMIZE
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
