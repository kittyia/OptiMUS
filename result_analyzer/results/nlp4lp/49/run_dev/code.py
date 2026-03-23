
import os
import numpy as np
import json 
from gurobipy import Model, GRB, quicksum


model = Model("OptimizationProblem")

with open("data.json", "r") as f:
    data = json.load(f)




### Define the parameters

MangoJuicePerMangoTea = data["MangoJuicePerMangoTea"] # shape: [], definition: Units of mango juice required to make one mango bubble tea

LycheeJuicePerLycheeTea = data["LycheeJuicePerLycheeTea"] # shape: [], definition: Units of lychee juice required to make one lychee bubble tea

TeaPerMangoTea = data["TeaPerMangoTea"] # shape: [], definition: Units of tea required to make one mango bubble tea

TeaPerLycheeTea = data["TeaPerLycheeTea"] # shape: [], definition: Units of tea required to make one lychee bubble tea

TotalMangoJuice = data["TotalMangoJuice"] # shape: [], definition: Total units of mango juice available

TotalLycheeJuice = data["TotalLycheeJuice"] # shape: [], definition: Total units of lychee juice available

MinLycheePercentage = data["MinLycheePercentage"] # shape: [], definition: Minimum percentage of total bubble teas that must be lychee flavored



### Define the variables

MangoTeas = model.addVar(vtype=GRB.INTEGER, name="MangoTeas")

LycheeTeas = model.addVar(vtype=GRB.INTEGER, name="LycheeTeas")



### Define the constraints

model.addConstr(MangoJuicePerMangoTea * MangoTeas <= TotalMangoJuice)
model.addConstr(LycheeJuicePerLycheeTea * LycheeTeas <= TotalLycheeJuice)
model.addConstr(LycheeTeas >= (2.0/3.0) * MangoTeas)
model.addConstr(MangoTeas >= LycheeTeas)


### Define the objective

del.setObjective(TeaPerMangoTea * MangoTeas + TeaPerLycheeTea * LycheeTeas, GRB.MINIMIZE


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
