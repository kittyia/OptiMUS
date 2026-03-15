
import os
import numpy as np
import json 
from gurobipy import Model, GRB, quicksum


model = Model("OptimizationProblem")

with open("data.json", "r") as f:
    data = json.load(f)




### Define the parameters

ChocolateMixPerBrownie = data["ChocolateMixPerBrownie"] # shape: [], definition: Amount of chocolate mix required to produce one brownie

FiberPerBrownie = data["FiberPerBrownie"] # shape: [], definition: Amount of fiber required to produce one brownie

LemonMixPerLemonSquare = data["LemonMixPerLemonSquare"] # shape: [], definition: Amount of lemon mix required to produce one lemon square

FiberPerLemonSquare = data["FiberPerLemonSquare"] # shape: [], definition: Amount of fiber required to produce one lemon square

TotalChocolateMix = data["TotalChocolateMix"] # shape: [], definition: Total units of chocolate mix available

TotalLemonMix = data["TotalLemonMix"] # shape: [], definition: Total units of lemon mix available

MinBrowniePercentage = data["MinBrowniePercentage"] # shape: [], definition: Minimum percentage of items that must be brownies

MinLemonExceedsBrownie = data["MinLemonExceedsBrownie"] # shape: [], definition: Minimum required difference between the number of lemon squares and brownies



### Define the variables

Brownies = model.addVar(vtype=GRB.INTEGER, name="Brownies")

LemonSquares = model.addVar(vtype=GRB.INTEGER, name="LemonSquares")



### Define the constraints

model.addConstr(ChocolateMixPerBrownie * Brownies <= TotalChocolateMix)
model.addConstr(LemonMixPerLemonSquare * LemonSquares <= TotalLemonMix)
model.addConstr(LemonSquares >= Brownies + 1)
model.addConstr(Brownies >= MinBrowniePercentage * (Brownies + LemonSquares))


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
