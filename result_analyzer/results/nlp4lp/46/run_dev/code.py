
import os
import numpy as np
import json 
from gurobipy import Model, GRB, quicksum


model = Model("OptimizationProblem")

with open("data.json", "r") as f:
    data = json.load(f)




### Define the parameters

MeatPerWrap = data["MeatPerWrap"] # shape: [], definition: Amount of meat required to produce one wrap

RicePerWrap = data["RicePerWrap"] # shape: [], definition: Amount of rice required to produce one wrap

MeatPerPlatter = data["MeatPerPlatter"] # shape: [], definition: Amount of meat required to produce one platter

RicePerPlatter = data["RicePerPlatter"] # shape: [], definition: Amount of rice required to produce one platter

TimePerWrap = data["TimePerWrap"] # shape: [], definition: Production time required to produce one wrap

TimePerPlatter = data["TimePerPlatter"] # shape: [], definition: Production time required to produce one platter

MinMeat = data["MinMeat"] # shape: [], definition: Minimum required amount of meat

MinRice = data["MinRice"] # shape: [], definition: Minimum required amount of rice

WrapPlatterRatio = data["WrapPlatterRatio"] # shape: [], definition: Minimum ratio of wraps to platters



### Define the variables

Wraps = model.addVar(vtype=GRB.INTEGER, name="Wraps")

Platters = model.addVar(vtype=GRB.INTEGER, name="Platters")



### Define the constraints

model.addConstr(MeatPerWrap * Wraps + MeatPerPlatter * Platters >= MinMeat)
model.addConstr(RicePerWrap * Wraps + RicePerPlatter * Platters >= MinRice)
model.addConstr(Wraps >= WrapPlatterRatio * Platters)
model.addConstr(Wraps >= 0)
model.addConstr(Platters >= 0)


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
