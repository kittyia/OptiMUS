
import os
import numpy as np
import json 
from gurobipy import Model, GRB, quicksum


model = Model("OptimizationProblem")

with open("data.json", "r") as f:
    data = json.load(f)




### Define the parameters

TotalLandAvailable = data["TotalLandAvailable"] # shape: [], definition: Total land available to grow crops

MinAcresPotatoes = data["MinAcresPotatoes"] # shape: [], definition: Minimum acres of potatoes required

MinAcresCucumbers = data["MinAcresCucumbers"] # shape: [], definition: Minimum acres of cucumbers required

MaxCucumbersPerPotatoesRatio = data["MaxCucumbersPerPotatoesRatio"] # shape: [], definition: Maximum ratio of cucumbers to potatoes that can be grown

ProfitPerAcrePotatoes = data["ProfitPerAcrePotatoes"] # shape: [], definition: Profit per acre of potatoes

ProfitPerAcreCucumbers = data["ProfitPerAcreCucumbers"] # shape: [], definition: Profit per acre of cucumbers



### Define the variables

AcresPotatoes = model.addVar(vtype=GRB.CONTINUOUS, name="AcresPotatoes")

AcresCucumbers = model.addVar(vtype=GRB.CONTINUOUS, name="AcresCucumbers")



### Define the constraints

model.addConstr(AcresPotatoes + AcresCucumbers <= TotalLandAvailable)
model.addConstr(AcresPotatoes >= MinAcresPotatoes)
model.addConstr(AcresCucumbers >= MinAcresCucumbers)
model.addConstr(AcresCucumbers <= MaxCucumbersPerPotatoesRatio * AcresPotatoes)


### Define the objective

model.setObjective(
    ProfitPerAcrePotatoes * AcresPotatoes + 
    ProfitPerAcreCucumbers * AcresCucumbers,
    GRB.MAXIMIZE
)


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
