
import os
import numpy as np
import json 
from gurobipy import Model, GRB, quicksum


model = Model("OptimizationProblem")

with open("data.json", "r") as f:
    data = json.load(f)




### Define the parameters

GoatMeatPerGoatCurry = data["GoatMeatPerGoatCurry"] # shape: [], definition: Units of goat meat required to produce one bowl of goat curry

ChickenMeatPerChickenCurry = data["ChickenMeatPerChickenCurry"] # shape: [], definition: Units of chicken meat required to produce one bowl of chicken curry

CurryBasePerGoatCurry = data["CurryBasePerGoatCurry"] # shape: [], definition: Units of curry base required to produce one bowl of goat curry

CurryBasePerChickenCurry = data["CurryBasePerChickenCurry"] # shape: [], definition: Units of curry base required to produce one bowl of chicken curry

TotalGoatMeatAvailable = data["TotalGoatMeatAvailable"] # shape: [], definition: Total available units of goat meat

TotalChickenMeatAvailable = data["TotalChickenMeatAvailable"] # shape: [], definition: Total available units of chicken meat

MinChickenCurryPercentage = data["MinChickenCurryPercentage"] # shape: [], definition: Minimum percentage of curry bowls that must be chicken curry



### Define the variables

goatCurryBowls = model.addVar(vtype=GRB.INTEGER, name="goatCurryBowls")

chickenCurryBowls = model.addVar(vtype=GRB.INTEGER, name="chickenCurryBowls")



### Define the constraints

model.addConstr(GoatMeatPerGoatCurry * goatCurryBowls <= TotalGoatMeatAvailable)
model.addConstr(ChickenMeatPerChickenCurry * chickenCurryBowls <= TotalChickenMeatAvailable)
model.addConstr(goatCurryBowls >= chickenCurryBowls + 1)
model.addConstr(goatCurryBowls <= 3 * chickenCurryBowls)
model.addConstr(goatCurryBowls >= 0)
model.addConstr(chickenCurryBowls >= 0)


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
