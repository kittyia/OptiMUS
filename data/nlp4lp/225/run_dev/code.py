
import os
import numpy as np
import json 
from gurobipy import Model, GRB, quicksum


model = Model("OptimizationProblem")

with open("data.json", "r") as f:
    data = json.load(f)




### Define the parameters

TotalResin = data["TotalResin"] # shape: [], definition: Total amount of resin available for filling cavities

ResinPerMolar = data["ResinPerMolar"] # shape: [], definition: Units of resin required to fill one molar

ResinPerCanine = data["ResinPerCanine"] # shape: [], definition: Units of resin required to fill one canine

PainKillerPerMolar = data["PainKillerPerMolar"] # shape: [], definition: Units of pain killer required to fill one molar

PainKillerPerCanine = data["PainKillerPerCanine"] # shape: [], definition: Units of pain killer required to fill one canine

MinPercentageCanines = data["MinPercentageCanines"] # shape: [], definition: Minimum fraction of cavities filled that must be canines

MinNumMolars = data["MinNumMolars"] # shape: [], definition: Minimum number of molars that must be filled



### Define the variables

M = model.addVar(vtype=GRB.INTEGER, name="M")

C = model.addVar(vtype=GRB.INTEGER, name="C")



### Define the constraints

model.addConstr(ResinPerMolar * M + ResinPerCanine * C <= TotalResin)
model.addConstr(C >= MinPercentageCanines * (M + C))
model.addConstr(M >= MinNumMolars)


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
