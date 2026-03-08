
import os
import numpy as np
import json 
from gurobipy import Model, GRB, quicksum


model = Model("OptimizationProblem")

with open("data.json", "r") as f:
    data = json.load(f)




### Define the parameters

NumProductTypes = data["NumProductTypes"] # shape: [], definition: Number of different product types

PlasticCostMechanical = data["PlasticCostMechanical"] # shape: [], definition: Units of plastic required to produce one mechanical keyboard

PlasticCostStandard = data["PlasticCostStandard"] # shape: [], definition: Units of plastic required to produce one standard keyboard

SolderCostMechanical = data["SolderCostMechanical"] # shape: [], definition: Units of solder required to produce one mechanical keyboard

SolderCostStandard = data["SolderCostStandard"] # shape: [], definition: Units of solder required to produce one standard keyboard

MechanicalToStandardRatio = data["MechanicalToStandardRatio"] # shape: [], definition: Desired ratio of mechanical keyboards to standard keyboards

MinimumStandardKeyboards = data["MinimumStandardKeyboards"] # shape: [], definition: Minimum number of standard keyboards to be produced

TotalPlasticAvailable = data["TotalPlasticAvailable"] # shape: [], definition: Total units of plastic available

TotalSolderAvailable = data["TotalSolderAvailable"] # shape: [], definition: Total units of solder available



### Define the variables

MechanicalKeyboards = model.addVar(vtype=GRB.INTEGER, name="MechanicalKeyboards")

StandardKeyboards = model.addVar(vtype=GRB.INTEGER, name="StandardKeyboards")



### Define the constraints

model.addConstr(
    PlasticCostMechanical * MechanicalKeyboards
    + PlasticCostStandard * StandardKeyboards
    <= TotalPlasticAvailable
)
model.addConstr(SolderCostMechanical * MechanicalKeyboards + SolderCostStandard * StandardKeyboards <= TotalSolderAvailable)
model.addConstr(MechanicalKeyboards == MechanicalToStandardRatio * StandardKeyboards)
model.addConstr(StandardKeyboards >= MinimumStandardKeyboards)


### Define the objective

model.setObjective(MechanicalKeyboards + StandardKeyboards, GRB.MAXIMIZE)


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
