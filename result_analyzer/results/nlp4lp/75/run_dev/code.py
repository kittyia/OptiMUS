
import os
import numpy as np
import json 
from gurobipy import Model, GRB, quicksum


model = Model("OptimizationProblem")

with open("data.json", "r") as f:
    data = json.load(f)




### Define the parameters

TotalLakeArea = data["TotalLakeArea"] # shape: [], definition: Total area of the lake in acres

FishPerAcreNet = data["FishPerAcreNet"] # shape: [], definition: Number of fish caught per acre using a net

BaitPerAcreNet = data["BaitPerAcreNet"] # shape: [], definition: Units of bait required per acre using a net

PainPerAcreNet = data["PainPerAcreNet"] # shape: [], definition: Units of pain caused per acre using a net

FishPerAcreLine = data["FishPerAcreLine"] # shape: [], definition: Number of fish caught per acre using a fishing line

BaitPerAcreLine = data["BaitPerAcreLine"] # shape: [], definition: Units of bait required per acre using a fishing line

PainPerAcreLine = data["PainPerAcreLine"] # shape: [], definition: Units of pain caused per acre using a fishing line

TotalAvailableBait = data["TotalAvailableBait"] # shape: [], definition: Total available units of bait

MaxTotalPain = data["MaxTotalPain"] # shape: [], definition: Maximum tolerable units of pain



### Define the variables

acresNet = model.addVar(vtype=GRB.CONTINUOUS, name="acresNet")

acresLine = model.addVar(vtype=GRB.CONTINUOUS, name="acresLine")



### Define the constraints

model.addConstr(acresNet + acresLine <= TotalLakeArea)
model.addConstr(BaitPerAcreNet * acresNet + BaitPerAcreLine * acresLine <= TotalAvailableBait)
model.addConstr(PainPerAcreNet * acresNet + PainPerAcreLine * acresLine <= MaxTotalPain)
model.addConstr(acresNet >= 0)
model.addConstr(acresLine >= 0)


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
