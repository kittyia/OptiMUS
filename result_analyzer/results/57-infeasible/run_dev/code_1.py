import os
import numpy as np
import json
from gurobipy import Model, GRB, quicksum


model = Model("OptimizationProblem")

with open("data.json", "r") as f:
    data = json.load(f)


### Define the parameters

GasPattiesPerMinute = data["GasPattiesPerMinute"]
ElectricPattiesPerMinute = data["ElectricPattiesPerMinute"]
GasOilPerMinute = data["GasOilPerMinute"]
ElectricOilPerMinute = data["ElectricOilPerMinute"]
MinPattiesPerMinute = data["MinPattiesPerMinute"]
MaxOilPerMinute = data["MaxOilPerMinute"]


### Define the variables

GasGrills = model.addVar(vtype=GRB.INTEGER, name="GasGrills", lb=0)
ElectricGrills = model.addVar(vtype=GRB.INTEGER, name="ElectricGrills", lb=0)


### Define the constraints

model.addConstr(GasPattiesPerMinute * GasGrills + 
                ElectricPattiesPerMinute * ElectricGrills >= MinPattiesPerMinute)

model.addConstr(GasOilPerMinute * GasGrills + 
                ElectricOilPerMinute * ElectricGrills <= MaxOilPerMinute)

model.addConstr(ElectricGrills <= GasGrills - 1)


### Define the objective

model.setObjective(GasGrills + ElectricGrills, GRB.MINIMIZE)


### Optimize the model

model.optimize()


### Output optimal objective value

if model.status == GRB.OPTIMAL:
    print("Optimal Objective Value: ", model.ObjVal)
    with open("output_solution.txt", "w") as f:
        f.write(str(model.ObjVal))
else:
    with open("output_solution.txt", "w") as f:
        f.write(str(model.status))
``