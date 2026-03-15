
import os
import numpy as np
import json 
from gurobipy import Model, GRB, quicksum


model = Model("OptimizationProblem")

with open("data.json", "r") as f:
    data = json.load(f)




### Define the parameters

AvailablePeachFlavoring = data["AvailablePeachFlavoring"] # shape: [], definition: Units of peach flavoring available

AvailableCherryFlavoring = data["AvailableCherryFlavoring"] # shape: [], definition: Units of cherry flavoring available

PeachFlavoringPerPack = data["PeachFlavoringPerPack"] # shape: [], definition: Units of peach flavoring required per pack of peach candy

CherryFlavoringPerPack = data["CherryFlavoringPerPack"] # shape: [], definition: Units of cherry flavoring required per pack of cherry candy

SpecialSyrupPerPackPeach = data["SpecialSyrupPerPackPeach"] # shape: [], definition: Units of special syrup required per pack of peach candy

SpecialSyrupPerPackCherry = data["SpecialSyrupPerPackCherry"] # shape: [], definition: Units of special syrup required per pack of cherry candy

MinimumCherryPercentage = data["MinimumCherryPercentage"] # shape: [], definition: Minimum fraction of packs that must be cherry flavored



### Define the variables

PeachPacks = model.addVar(vtype=GRB.INTEGER, name="PeachPacks")

CherryPacks = model.addVar(vtype=GRB.INTEGER, name="CherryPacks")



### Define the constraints

model.addConstr(PeachFlavoringPerPack * PeachPacks <= AvailablePeachFlavoring)
model.addConstr(CherryFlavoringPerPack * CherryPacks <= AvailableCherryFlavoring)
model.addConstr(PeachPacks >= CherryPacks)
model.addConstr(CherryPacks >= MinimumCherryPercentage * (PeachPacks + CherryPacks))
model.addConstr(PeachPacks >= 0)
model.addConstr(CherryPacks >= 0)


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
