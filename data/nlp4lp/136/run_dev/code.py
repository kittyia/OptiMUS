
import os
import numpy as np
import json 
from gurobipy import Model, GRB, quicksum


model = Model("OptimizationProblem")

with open("data.json", "r") as f:
    data = json.load(f)




### Define the parameters

AntiOxidantsPerBlueberryPack = data["AntiOxidantsPerBlueberryPack"] # shape: [], definition: Units of anti-oxidants per pack of blueberries

AntiOxidantsPerStrawberryPack = data["AntiOxidantsPerStrawberryPack"] # shape: [], definition: Units of anti-oxidants per pack of strawberries

MineralsPerBlueberryPack = data["MineralsPerBlueberryPack"] # shape: [], definition: Units of minerals per pack of blueberries

MineralsPerStrawberryPack = data["MineralsPerStrawberryPack"] # shape: [], definition: Units of minerals per pack of strawberries

SugarPerBlueberryPack = data["SugarPerBlueberryPack"] # shape: [], definition: Grams of sugar per pack of blueberries

SugarPerStrawberryPack = data["SugarPerStrawberryPack"] # shape: [], definition: Grams of sugar per pack of strawberries

MinimumAntiOxidants = data["MinimumAntiOxidants"] # shape: [], definition: Minimum required units of anti-oxidants

MinimumMinerals = data["MinimumMinerals"] # shape: [], definition: Minimum required units of minerals

MinimumStrawberriesToBlueberriesRatio = data["MinimumStrawberriesToBlueberriesRatio"] # shape: [], definition: Minimum ratio of strawberries packs to blueberry packs



### Define the variables

BlueberryPacks = model.addVar(vtype=GRB.INTEGER, name="BlueberryPacks")

StrawberryPacks = model.addVar(vtype=GRB.INTEGER, name="StrawberryPacks")



### Define the constraints

model.addConstr(
    AntiOxidantsPerBlueberryPack * BlueberryPacks +
    AntiOxidantsPerStrawberryPack * StrawberryPacks
    >= MinimumAntiOxidants
)
model.addConstr(StrawberryPacks >= MinimumStrawberriesToBlueberriesRatio * BlueberryPacks)
model.addConstr(BlueberryPacks >= 0)


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
