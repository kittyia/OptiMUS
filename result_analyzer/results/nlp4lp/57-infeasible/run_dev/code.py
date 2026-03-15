
import os
import numpy as np
import json 
from gurobipy import Model, GRB, quicksum


model = Model("OptimizationProblem")

with open("data.json", "r") as f:
    data = json.load(f)




### Define the parameters

GasPattiesPerMinute = data["GasPattiesPerMinute"] # shape: [], definition: GasPattiesPerMinute

ElectricPattiesPerMinute = data["ElectricPattiesPerMinute"] # shape: [], definition: ElectricPattiesPerMinute

GasOilPerMinute = data["GasOilPerMinute"] # shape: [], definition: GasOilPerMinute

ElectricOilPerMinute = data["ElectricOilPerMinute"] # shape: [], definition: ElectricOilPerMinute

MinPattiesPerMinute = data["MinPattiesPerMinute"] # shape: [], definition: MinPattiesPerMinute

MaxOilPerMinute = data["MaxOilPerMinute"] # shape: [], definition: MaxOilPerMinute



### Define the variables

GasGrills = model.addVar(vtype=GRB.INTEGER, name="GasGrills")

ElectricGrills = model.addVar(vtype=GRB.INTEGER, name="ElectricGrills")



### Define the constraints

model.addConstr(GasPattiesPerMinute * GasGrills + ElectricPattiesPerMinute * ElectricGrills >= MinPattiesPerMinute)
model.addConstr(GasOilPerMinute * GasGrills + ElectricOilPerMinute * ElectricGrills <= MaxOilPerMinute)
model.addConstr(ElectricGrills <= GasGrills - 1)


### Define the objective

model.setObjective(GasGrills + ElectricGrills, GRB.MINIMIZE)


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
