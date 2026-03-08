
import os
import numpy as np
import json 
from gurobipy import Model, GRB, quicksum


model = Model("OptimizationProblem")

with open("data.json", "r") as f:
    data = json.load(f)




### Define the parameters

NumMachines = data["NumMachines"] # shape: [], definition: Number of machines

NumProducts = data["NumProducts"] # shape: [], definition: Number of products

ProductionRate = data["ProductionRate"] # shape: ['NumMachines', 'NumProducts'], definition: Amount of product p produced per hour by machine m

WaterUsage = data["WaterUsage"] # shape: ['NumMachines'], definition: Amount of distilled water consumed per hour by machine m

TotalWaterAvailable = data["TotalWaterAvailable"] # shape: [], definition: Total amount of distilled water available

RequiredProduct = data["RequiredProduct"] # shape: ['NumProducts'], definition: Minimum required amount of product p



### Define the variables

HoursUsed = model.addVars(NumMachines, vtype=GRB.CONTINUOUS, name="HoursUsed")



### Define the constraints

model.addConstr(30 * HoursUsed[0] + 45 * HoursUsed[1] >= 1300)
model.addConstr(60 * HoursUsed[0] + 30 * HoursUsed[1] >= 1500)
model.addConstr(
    sum(WaterUsage[m] * HoursUsed[m] for m in range(NumMachines)) 
    <= TotalWaterAvailable
)
model.addConstr(HoursUsed[0] >= 0)
model.addConstr(HoursUsed[1] >= 0)


### Define the objective

model.setObjective(quicksum(HoursUsed[m] for m in range(NumMachines)), GRB.MINIMIZE)


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
