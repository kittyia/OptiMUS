import os
import numpy as np
import json
from gurobipy import Model, GRB, quicksum


model = Model("OptimizationProblem")

with open("data.json", "r") as f:
    data = json.load(f)


### Define the parameters

MinimumVitaminA = data["MinimumVitaminA"]
MinimumVitaminC = data["MinimumVitaminC"]

VitaminAPerCrabCake = data["VitaminAPerCrabCake"]
VitaminCPerCrabCake = data["VitaminCPerCrabCake"]

VitaminAPerLobsterRoll = data["VitaminAPerLobsterRoll"]
VitaminCPerLobsterRoll = data["VitaminCPerLobsterRoll"]

UnsaturatedFatPerCrabCake = data["UnsaturatedFatPerCrabCake"]
UnsaturatedFatPerLobsterRoll = data["UnsaturatedFatPerLobsterRoll"]

MaximumLobsterFraction = data["MaximumLobsterFraction"]


### Define the variables

CrabCakes = model.addVar(vtype=GRB.INTEGER, name="CrabCakes", lb=0)
LobsterRolls = model.addVar(vtype=GRB.INTEGER, name="LobsterRolls", lb=0)


### Define the constraints

model.addConstr(
    VitaminAPerCrabCake * CrabCakes + 
    VitaminAPerLobsterRoll * LobsterRolls >= MinimumVitaminA
)

model.addConstr(
    VitaminCPerCrabCake * CrabCakes + 
    VitaminCPerLobsterRoll * LobsterRolls >= MinimumVitaminC
)

model.addConstr(
    LobsterRolls <= MaximumLobsterFraction * (CrabCakes + LobsterRolls)
)


### Define the objective

model.setObjective(
    UnsaturatedFatPerCrabCake * CrabCakes + 
    UnsaturatedFatPerLobsterRoll * LobsterRolls,
    GRB.MINIMIZE
)


### Optimize the model

model.optimize()


### Output optimal objective value

if model.status == GRB.OPTIMAL:
    print("Optimal Objective Value: ", model.objVal)
    with open("output_solution.txt", "w") as f:
        f.write(str(model.objVal))
else:
    with open("output_solution.txt", "w") as f:
        f.write(str(model.status))