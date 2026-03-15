
import os
import numpy as np
import json 
from gurobipy import Model, GRB, quicksum


model = Model("OptimizationProblem")

with open("data.json", "r") as f:
    data = json.load(f)




### Define the parameters

ChocolateSpreadPerChocolateCrepe = data["ChocolateSpreadPerChocolateCrepe"] # shape: [], definition: Amount of chocolate spread required to make one chocolate crepe

PeanutButterSpreadPerPeanutButterCrepe = data["PeanutButterSpreadPerPeanutButterCrepe"] # shape: [], definition: Amount of peanut butter spread required to make one peanut butter crepe

CrepeMixPerChocolateCrepe = data["CrepeMixPerChocolateCrepe"] # shape: [], definition: Amount of crepe mix required to make one chocolate crepe

CrepeMixPerPeanutButterCrepe = data["CrepeMixPerPeanutButterCrepe"] # shape: [], definition: Amount of crepe mix required to make one peanut butter crepe

TotalAvailableChocolateSpread = data["TotalAvailableChocolateSpread"] # shape: [], definition: Total available units of chocolate spread

TotalAvailablePeanutButterSpread = data["TotalAvailablePeanutButterSpread"] # shape: [], definition: Total available units of peanut butter spread

MinimumProportionChocolateCrepes = data["MinimumProportionChocolateCrepes"] # shape: [], definition: Minimum proportion of crepes that must be chocolate



### Define the variables

ChocolateCrepes = model.addVar(vtype=GRB.INTEGER, name="ChocolateCrepes")

PeanutButterCrepes = model.addVar(vtype=GRB.INTEGER, name="PeanutButterCrepes")



### Define the constraints

model.addConstr(ChocolateSpreadPerChocolateCrepe * ChocolateCrepes <= TotalAvailableChocolateSpread)
model.addConstr(4 * PeanutButterCrepes <= TotalAvailablePeanutButterSpread)
model.addConstr(PeanutButterCrepes >= ChocolateCrepes)
model.addConstr(ChocolateCrepes >= MinimumProportionChocolateCrepes * (ChocolateCrepes + PeanutButterCrepes))
model.addConstr(ChocolateCrepes >= 0)
model.addConstr(PeanutButterCrepes >= 0)


### Define the objective

del.setObjective(
    CrepeMixPerChocolateCrepe * ChocolateCrepes +
    CrepeMixPerPeanutButterCrepe * PeanutButterCrepes,
    GRB.MINIMIZE


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
