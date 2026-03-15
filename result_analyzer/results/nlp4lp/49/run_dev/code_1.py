import os
import numpy as np
import json 
from gurobipy import Model, GRB, quicksum


model = Model("OptimizationProblem")

with open("data.json", "r") as f:
    data = json.load(f)


### Define the parameters

MangoJuicePerMangoTea = data["MangoJuicePerMangoTea"]
LycheeJuicePerLycheeTea = data["LycheeJuicePerLycheeTea"]
TeaPerMangoTea = data["TeaPerMangoTea"]
TeaPerLycheeTea = data["TeaPerLycheeTea"]
TotalMangoJuice = data["TotalMangoJuice"]
TotalLycheeJuice = data["TotalLycheeJuice"]
MinLycheePercentage = data["MinLycheePercentage"]


### Define the variables

MangoTeas = model.addVar(vtype=GRB.INTEGER, lb=0, name="MangoTeas")
LycheeTeas = model.addVar(vtype=GRB.INTEGER, lb=0, name="LycheeTeas")


### Define the constraints

model.addConstr(MangoJuicePerMangoTea * MangoTeas <= TotalMangoJuice)
model.addConstr(LycheeJuicePerLycheeTea * LycheeTeas <= TotalLycheeJuice)

# At least 40% must be lychee flavored:
# LycheeTeas >= MinLycheePercentage * (MangoTeas + LycheeTeas)
model.addConstr(LycheeTeas >= MinLycheePercentage * (MangoTeas + LycheeTeas))

# Mango teas must be greater than or equal to lychee teas
model.addConstr(MangoTeas >= LycheeTeas)


### Define the objective

model.setObjective(
    TeaPerMangoTea * MangoTeas + TeaPerLycheeTea * LycheeTeas,
    GRB.MINIMIZE
)


### Optimize the model

model.optimize()


### Output optimal objective value

if model.status == GRB.OPTIMAL:
    print("Optimal Objective Value: ", model.objVal)
    with open("output_solution.txt", "w") as f:
        f.write(str(model.objVal))
else:
    with open("output_solution.txt", "w") as f:
        f.write(str(model.status))
``