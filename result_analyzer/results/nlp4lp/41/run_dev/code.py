
import os
import numpy as np
import json 
from gurobipy import Model, GRB, quicksum


model = Model("OptimizationProblem")

with open("data.json", "r") as f:
    data = json.load(f)




### Define the parameters

GemsPerHigh = data["GemsPerHigh"] # shape: [], definition: Number of gems processed per day by a high intensity drill.

WaterPerHigh = data["WaterPerHigh"] # shape: [], definition: Units of water required per day to dissipate heat by a high intensity drill.

GemsPerLow = data["GemsPerLow"] # shape: [], definition: Number of gems processed per day by a low intensity drill.

WaterPerLow = data["WaterPerLow"] # shape: [], definition: Units of water required per day to dissipate heat by a low intensity drill.

TotalGems = data["TotalGems"] # shape: [], definition: Total number of gems that must be processed per day by the factory.

AvailableWater = data["AvailableWater"] # shape: [], definition: Total units of water available per day for dissipating heat.

MaxHighFraction = data["MaxHighFraction"] # shape: [], definition: Maximum fraction of drills that can be high intensity to limit noise pollution.

MinLowDrills = data["MinLowDrills"] # shape: [], definition: Minimum number of low intensity drills that must be used.



### Define the variables

HighDrills = model.addVar(vtype=GRB.INTEGER, name="HighDrills")

LowDrills = model.addVar(vtype=GRB.INTEGER, name="LowDrills")



### Define the constraints

model.addConstr(GemsPerHigh * HighDrills + GemsPerLow * LowDrills >= TotalGems)
model.addConstr(WaterPerHigh * HighDrills + WaterPerLow * LowDrills <= AvailableWater)
model.addConstr(3 * HighDrills <= 2 * LowDrills)
model.addConstr(LowDrills >= MinLowDrills)
model.addConstr(HighDrills >= 0)
model.addConstr(HighDrills >= 0)
model.addConstr(LowDrills >= 0)


### Define the objective

model.setObjective(HighDrills + LowDrills, GRB.MINIMIZE)


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
