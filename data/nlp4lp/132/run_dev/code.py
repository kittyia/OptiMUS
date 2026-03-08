
import os
import numpy as np
import json 
from gurobipy import Model, GRB, quicksum


model = Model("OptimizationProblem")

with open("data.json", "r") as f:
    data = json.load(f)




### Define the parameters

NumExperiments = data["NumExperiments"] # shape: [], definition: Number of different experiments

RedUsage = data["RedUsage"] # shape: ['NumExperiments'], definition: Amount of red liquid required for each experiment

BlueUsage = data["BlueUsage"] # shape: ['NumExperiments'], definition: Amount of blue liquid required for each experiment

GreenGasProduction = data["GreenGasProduction"] # shape: ['NumExperiments'], definition: Amount of green gas produced by each experiment

SmellyGasProduction = data["SmellyGasProduction"] # shape: ['NumExperiments'], definition: Amount of smelly gas produced by each experiment

TotalRed = data["TotalRed"] # shape: [], definition: Total units of red liquid available

TotalBlue = data["TotalBlue"] # shape: [], definition: Total units of blue liquid available

MaxSmelly = data["MaxSmelly"] # shape: [], definition: Maximum units of smelly gas allowed



### Define the variables

Experiments = model.addVars(NumExperiments, vtype=GRB.INTEGER, name="Experiments")



### Define the constraints

model.addConstr(
    sum(SmellyGasProduction[i] * Experiments[i] for i in range(NumExperiments)) <= MaxSmelly
)
model.addConstr(Experiments[0] >= 0)
model.addConstr(Experiments[1] >= 0)


### Define the objective

model.setObjective(quicksum(GreenGasProduction[i] * Experiments[i] for i in range(NumExperiments)), GRB.MAXIMIZE)


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
