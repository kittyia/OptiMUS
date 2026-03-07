
import os
import numpy as np
import json 
from gurobipy import Model, GRB, quicksum


model = Model("OptimizationProblem")

with open("data.json", "r") as f:
    data = json.load(f)




### Define the parameters

DemandDeskLamps = data["DemandDeskLamps"] # shape: [], definition: Minimum expected demand for desk-lamps per day

DemandNightLamps = data["DemandNightLamps"] # shape: [], definition: Minimum expected demand for night-lamps per day

MaxDeskLamps = data["MaxDeskLamps"] # shape: [], definition: Maximum production capacity for desk-lamps per day

MaxNightLamps = data["MaxNightLamps"] # shape: [], definition: Maximum production capacity for night-lamps per day

MinTotalLamps = data["MinTotalLamps"] # shape: [], definition: Minimum total lamps to produce per day to satisfy contract

ProfitDeskLamp = data["ProfitDeskLamp"] # shape: [], definition: Profit per desk-lamp sold

ProfitNightLamp = data["ProfitNightLamp"] # shape: [], definition: Profit per night-lamp sold



### Define the variables

deskLampsProduced = model.addVar(vtype=GRB.INTEGER, name="deskLampsProduced")

nightLampsProduced = model.addVar(vtype=GRB.INTEGER, name="nightLampsProduced")



### Define the constraints

model.addConstr(deskLampsProduced >= DemandDeskLamps)
model.addConstr(deskLampsProduced <= MaxDeskLamps)
model.addConstr(nightLampsProduced >= DemandNightLamps)
model.addConstr(nightLampsProduced <= MaxNightLamps)
model.addConstr(deskLampsProduced + nightLampsProduced >= MinTotalLamps)


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
