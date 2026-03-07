
import os
import numpy as np
import json 
from gurobipy import Model, GRB, quicksum


model = Model("OptimizationProblem")

with open("data.json", "r") as f:
    data = json.load(f)




### Define the parameters

AvailablePaint = data["AvailablePaint"] # shape: [], definition: Total units of paint available

AvailableGlitter = data["AvailableGlitter"] # shape: [], definition: Total units of glitter available

AvailableGlue = data["AvailableGlue"] # shape: [], definition: Total units of glue available

PaintPerLarge = data["PaintPerLarge"] # shape: [], definition: Units of paint required to make one large art piece

GlitterPerLarge = data["GlitterPerLarge"] # shape: [], definition: Units of glitter required to make one large art piece

GluePerLarge = data["GluePerLarge"] # shape: [], definition: Units of glue required to make one large art piece

PaintPerSmall = data["PaintPerSmall"] # shape: [], definition: Units of paint required to make one small art piece

GlitterPerSmall = data["GlitterPerSmall"] # shape: [], definition: Units of glitter required to make one small art piece

GluePerSmall = data["GluePerSmall"] # shape: [], definition: Units of glue required to make one small art piece

ProfitLarge = data["ProfitLarge"] # shape: [], definition: Profit per large art piece

ProfitSmall = data["ProfitSmall"] # shape: [], definition: Profit per small art piece

MinLarge = data["MinLarge"] # shape: [], definition: Minimum number of large art pieces to produce

MinSmall = data["MinSmall"] # shape: [], definition: Minimum number of small art pieces to produce



### Define the variables

Large = model.addVar(vtype=GRB.INTEGER, name="Large")

Small = model.addVar(vtype=GRB.INTEGER, name="Small")



### Define the constraints

model.addConstr(4 * Large + 2 * Small <= AvailablePaint)
model.addConstr(3 * Large + Small <= AvailableGlitter)
model.addConstr(5 * Large + 2 * Small <= AvailableGlue)
model.addConstr(Large >= MinLarge)
model.addConstr(Small >= MinSmall)


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
