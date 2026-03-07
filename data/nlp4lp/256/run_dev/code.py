
import os
import numpy as np
import json 
from gurobipy import Model, GRB, quicksum


model = Model("OptimizationProblem")

with open("data.json", "r") as f:
    data = json.load(f)




### Define the parameters

AcaiBerriesAvailable = data["AcaiBerriesAvailable"] # shape: [], definition: Total units of acai berries available

BananaChocolateAvailable = data["BananaChocolateAvailable"] # shape: [], definition: Total units of banana chocolate available

AcaiBerriesPerAcaiSmoothie = data["AcaiBerriesPerAcaiSmoothie"] # shape: [], definition: Units of acai berries required per acai berry smoothie

WaterPerAcaiSmoothie = data["WaterPerAcaiSmoothie"] # shape: [], definition: Units of water required per acai berry smoothie

BananaChocolatePerBananaSmoothie = data["BananaChocolatePerBananaSmoothie"] # shape: [], definition: Units of banana chocolate required per banana chocolate smoothie

WaterPerBananaSmoothie = data["WaterPerBananaSmoothie"] # shape: [], definition: Units of water required per banana chocolate smoothie

MinAcaiProportion = data["MinAcaiProportion"] # shape: [], definition: Minimum proportion of smoothies that must be acai berry smoothies



### Define the variables

AcaiSmoothies = model.addVar(vtype=GRB.INTEGER, name="AcaiSmoothies")

BananaSmoothies = model.addVar(vtype=GRB.INTEGER, name="BananaSmoothies")



### Define the constraints

model.addConstr(AcaiBerriesPerAcaiSmoothie * AcaiSmoothies <= AcaiBerriesAvailable)
model.addConstr(6 * BananaSmoothies <= 3200)
model.addConstr(BananaSmoothies >= AcaiSmoothies)
model.addConstr(AcaiSmoothies >= MinAcaiProportion * (AcaiSmoothies + BananaSmoothies))
model.addConstr(AcaiSmoothies >= 0)
model.addConstr(BananaSmoothies >= 0)


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
