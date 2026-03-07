
import os
import numpy as np
import json 
from gurobipy import Model, GRB, quicksum


model = Model("OptimizationProblem")

with open("data.json", "r") as f:
    data = json.load(f)




### Define the parameters

ProfitPerChair = data["ProfitPerChair"] # shape: [], definition: Profit per chair

ProfitPerDresser = data["ProfitPerDresser"] # shape: [], definition: Profit per dresser

AvailableStain = data["AvailableStain"] # shape: [], definition: Available gallons of stain per week

AvailableOak = data["AvailableOak"] # shape: [], definition: Available lengths of oak wood per week

StainPerChair = data["StainPerChair"] # shape: [], definition: Gallons of stain required to produce one chair

StainPerDresser = data["StainPerDresser"] # shape: [], definition: Gallons of stain required to produce one dresser

OakPerChair = data["OakPerChair"] # shape: [], definition: Lengths of oak wood required to produce one chair

OakPerDresser = data["OakPerDresser"] # shape: [], definition: Lengths of oak wood required to produce one dresser



### Define the variables

NumChairs = model.addVar(vtype=GRB.INTEGER, name="NumChairs")

NumDressers = model.addVar(vtype=GRB.INTEGER, name="NumDressers")



### Define the constraints

model.addConstr(StainPerChair * NumChairs + StainPerDresser * NumDressers <= AvailableStain)
model.addConstr(OakPerChair * NumChairs + OakPerDresser * NumDressers <= AvailableOak)
model.addConstr(NumChairs >= 0)
model.addConstr(NumDressers >= 0)


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
