
import os
import numpy as np
import json 
from gurobipy import Model, GRB, quicksum


model = Model("OptimizationProblem")

with open("data.json", "r") as f:
    data = json.load(f)




### Define the parameters

FruitPerWine = data["FruitPerWine"] # shape: [], definition: Units of fruit needed for one unit of wine

WaterPerWine = data["WaterPerWine"] # shape: [], definition: Units of water needed for one unit of wine

FruitPerKombucha = data["FruitPerKombucha"] # shape: [], definition: Units of fruit needed for one unit of kombucha

TeaPerKombucha = data["TeaPerKombucha"] # shape: [], definition: Units of tea needed for one unit of kombucha

TotalWater = data["TotalWater"] # shape: [], definition: Total available units of water

TotalTea = data["TotalTea"] # shape: [], definition: Total available units of tea

MinKombuchaPercentage = data["MinKombuchaPercentage"] # shape: [], definition: Minimum percentage of products made that must be kombucha



### Define the variables

Wine = model.addVar(vtype=GRB.CONTINUOUS, name="Wine")

Kombucha = model.addVar(vtype=GRB.CONTINUOUS, name="Kombucha")



### Define the constraints

model.addConstr(WaterPerWine * Wine <= TotalWater)
model.addConstr(TeaPerKombucha * Kombucha <= TotalTea)
model.addConstr(Wine >= Kombucha)
model.addConstr(Kombucha >= MinKombuchaPercentage * (Wine + Kombucha))


### Define the objective

model.setObjective(FruitPerWine * Wine + FruitPerKombucha * Kombucha, GRB.MINIMIZE)


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
