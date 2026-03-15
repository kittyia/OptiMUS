
import os
import numpy as np
import json 
from gurobipy import Model, GRB, quicksum


model = Model("OptimizationProblem")

with open("data.json", "r") as f:
    data = json.load(f)




### Define the parameters

WoodPerTrain = data["WoodPerTrain"] # shape: [], definition: Amount of wood required to produce one model train

PaintPerTrain = data["PaintPerTrain"] # shape: [], definition: Amount of paint required to produce one model train

WoodPerPlane = data["WoodPerPlane"] # shape: [], definition: Amount of wood required to produce one model plane

PaintPerPlane = data["PaintPerPlane"] # shape: [], definition: Amount of paint required to produce one model plane

AvailableWood = data["AvailableWood"] # shape: [], definition: Total available units of wood

AvailablePaint = data["AvailablePaint"] # shape: [], definition: Total available units of paint

ProfitTrain = data["ProfitTrain"] # shape: [], definition: Profit earned per model train

ProfitPlane = data["ProfitPlane"] # shape: [], definition: Profit earned per model plane



### Define the variables

NumTrains = model.addVar(vtype=GRB.INTEGER, name="NumTrains")

NumPlanes = model.addVar(vtype=GRB.INTEGER, name="NumPlanes")



### Define the constraints

model.addConstr(WoodPerTrain * NumTrains + WoodPerPlane * NumPlanes <= AvailableWood)
model.addConstr(PaintPerTrain * NumTrains + PaintPerPlane * NumPlanes <= AvailablePaint)
model.addConstr(NumTrains >= 0)
model.addConstr(NumPlanes >= 0)


### Define the objective

model.setObjective(ProfitTrain * NumTrains + ProfitPlane * NumPlanes, GRB.MAXIMIZE)


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
