
import os
import numpy as np
import json 
from gurobipy import Model, GRB, quicksum


model = Model("OptimizationProblem")

with open("data.json", "r") as f:
    data = json.load(f)




### Define the parameters

NumMethods = data["NumMethods"] # shape: [], definition: The number of production methods available

NumProducts = data["NumProducts"] # shape: [], definition: The number of different products being produced

ProductionRate = data["ProductionRate"] # shape: ['NumProducts', 'NumMethods'], definition: Units of each product produced per hour by each method

SpecialElementConsumption = data["SpecialElementConsumption"] # shape: ['NumMethods'], definition: Units of the special element required per hour by each method

TotalSpecialElement = data["TotalSpecialElement"] # shape: [], definition: Total units of the special element available

MinRequired = data["MinRequired"] # shape: ['NumProducts'], definition: Minimum number of units required for each product



### Define the variables

MethodHours = model.addVars(NumMethods, vtype=GRB.CONTINUOUS, name="MethodHours")



### Define the constraints

model.addConstr(
    sum(SpecialElementConsumption[m] * MethodHours[m] for m in range(NumMethods))
    <= TotalSpecialElement
)
model.addConstr(
    sum(ProductionRate[0][m] * MethodHours[m] for m in range(NumMethods)) >= 1400
)
model.addConstr(
    sum(ProductionRate[1][m] * MethodHours[m] for m in range(NumMethods)) >= 1000
)
for m in range(NumMethods):
    model.addConstr(MethodHours[m] >= 0)


### Define the objective

model.setObjective(quicksum(MethodHours[m] for m in range(NumMethods)), GRB.MINIMIZE)


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
