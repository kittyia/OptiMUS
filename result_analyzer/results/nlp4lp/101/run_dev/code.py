
import os
import numpy as np
import json 
from gurobipy import Model, GRB, quicksum


model = Model("OptimizationProblem")

with open("data.json", "r") as f:
    data = json.load(f)




### Define the parameters

MinimumVitaminA = data["MinimumVitaminA"] # shape: [], definition: Minimum required units of vitamin A

MinimumVitaminC = data["MinimumVitaminC"] # shape: [], definition: Minimum required units of vitamin C

VitaminAPerCrabCake = data["VitaminAPerCrabCake"] # shape: [], definition: Units of vitamin A per crab cake

VitaminCPerCrabCake = data["VitaminCPerCrabCake"] # shape: [], definition: Units of vitamin C per crab cake

VitaminAPerLobsterRoll = data["VitaminAPerLobsterRoll"] # shape: [], definition: Units of vitamin A per lobster roll

VitaminCPerLobsterRoll = data["VitaminCPerLobsterRoll"] # shape: [], definition: Units of vitamin C per lobster roll

UnsaturatedFatPerCrabCake = data["UnsaturatedFatPerCrabCake"] # shape: [], definition: Units of unsaturated fat per crab cake

UnsaturatedFatPerLobsterRoll = data["UnsaturatedFatPerLobsterRoll"] # shape: [], definition: Units of unsaturated fat per lobster roll

MaximumLobsterFraction = data["MaximumLobsterFraction"] # shape: [], definition: Maximum fraction of meals that can be lobster rolls



### Define the variables

CrabCakes = model.addVar(vtype=GRB.CONTINUOUS, name="CrabCakes")

LobsterRolls = model.addVar(vtype=GRB.CONTINUOUS, name="LobsterRolls")



### Define the constraints

model.addConstr(VitaminAPerCrabCake * CrabCakes + VitaminAPerLobsterRoll * LobsterRolls >= MinimumVitaminA)
model.addConstr(7 * CrabCakes + 4 * LobsterRolls >= MinimumVitaminC)
model.addConstr(LobsterRolls <= MaximumLobsterFraction * (CrabCakes + LobsterRolls))
model.addConstr(CrabCakes >= 0)
model.addConstr(LobsterRolls >= 0)


### Define the objective

model.setObjective(UnsaturatedFatPerCrabCake * CrabCakes + UnsaturatedFatPerLobsterRoll * LobsterRolls, GRB.MINIMIZE)


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
