
import os
import numpy as np
import json 
from gurobipy import Model, GRB, quicksum


model = Model("OptimizationProblem")

with open("data.json", "r") as f:
    data = json.load(f)




### Define the parameters

CocoaPerMilkBar = data["CocoaPerMilkBar"] # shape: [], definition: Amount of cocoa required to produce one milk chocolate bar

MilkPerMilkBar = data["MilkPerMilkBar"] # shape: [], definition: Amount of milk required to produce one milk chocolate bar

CocoaPerDarkBar = data["CocoaPerDarkBar"] # shape: [], definition: Amount of cocoa required to produce one dark chocolate bar

MilkPerDarkBar = data["MilkPerDarkBar"] # shape: [], definition: Amount of milk required to produce one dark chocolate bar

TotalCocoa = data["TotalCocoa"] # shape: [], definition: Total units of cocoa available

TotalMilk = data["TotalMilk"] # shape: [], definition: Total units of milk available

MinMilkToDarkRatio = data["MinMilkToDarkRatio"] # shape: [], definition: Minimum ratio of milk chocolate bars to dark chocolate bars

TimePerMilkBar = data["TimePerMilkBar"] # shape: [], definition: Time required to produce one milk chocolate bar in minutes

TimePerDarkBar = data["TimePerDarkBar"] # shape: [], definition: Time required to produce one dark chocolate bar in minutes



### Define the variables

milkBars = model.addVar(vtype=GRB.INTEGER, name="milkBars")

darkBars = model.addVar(vtype=GRB.INTEGER, name="darkBars")



### Define the constraints

model.addConstr(CocoaPerMilkBar * milkBars + CocoaPerDarkBar * darkBars <= TotalCocoa)
model.addConstr(MilkPerMilkBar * milkBars + MilkPerDarkBar * darkBars <= TotalMilk)
model.addConstr(milkBars >= MinMilkToDarkRatio * darkBars)
model.addConstr(milkBars >= 0)
model.addConstr(darkBars >= 0)


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
