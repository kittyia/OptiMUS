
import os
import numpy as np
import json 
from gurobipy import Model, GRB, quicksum


model = Model("OptimizationProblem")

with open("data.json", "r") as f:
    data = json.load(f)




### Define the parameters

TotalGold = data["TotalGold"] # shape: [], definition: Total amount of gold available

GoldPerLong = data["GoldPerLong"] # shape: [], definition: Amount of gold required to produce one long cable

GoldPerShort = data["GoldPerShort"] # shape: [], definition: Amount of gold required to produce one short cable

MinShortToLongRatio = data["MinShortToLongRatio"] # shape: [], definition: Minimum ratio of the number of short cables to long cables

MinLongCables = data["MinLongCables"] # shape: [], definition: Minimum number of long cables to be made

ProfitPerLong = data["ProfitPerLong"] # shape: [], definition: Profit earned per long cable sold

ProfitPerShort = data["ProfitPerShort"] # shape: [], definition: Profit earned per short cable sold



### Define the variables

LongCables = model.addVar(vtype=GRB.INTEGER, name="LongCables")

ShortCables = model.addVar(vtype=GRB.INTEGER, name="ShortCables")



### Define the constraints

model.addConstr(GoldPerLong * LongCables + GoldPerShort * ShortCables <= TotalGold)
model.addConstr(ShortCables >= MinShortToLongRatio * LongCables)
model.addConstr(LongCables >= MinLongCables)
LongCables.vtype = GRB.INTEGER
ShortCables.vtype = GRB.INTEGER


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
