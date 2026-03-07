
import os
import numpy as np
import json 
from gurobipy import Model, GRB, quicksum


model = Model("OptimizationProblem")

with open("data.json", "r") as f:
    data = json.load(f)




### Define the parameters

TimePerUnitSulfate = data["TimePerUnitSulfate"] # shape: [], definition: Time taken for one unit of sulfate to be effective

TimePerUnitGinger = data["TimePerUnitGinger"] # shape: [], definition: Time taken for one unit of ginger to be effective

MinSulfateUnits = data["MinSulfateUnits"] # shape: [], definition: Minimum required units of sulfate

TotalUnits = data["TotalUnits"] # shape: [], definition: Total units of sulfate and ginger

MaxSulfateToGingerRatio = data["MaxSulfateToGingerRatio"] # shape: [], definition: Maximum allowed ratio of sulfate to ginger



### Define the variables

SulfateUnits = model.addVar(vtype=GRB.CONTINUOUS, name="SulfateUnits")

GingerUnits = model.addVar(vtype=GRB.CONTINUOUS, name="GingerUnits")



### Define the constraints

model.addConstr(SulfateUnits >= MinSulfateUnits)
model.addConstr(SulfateUnits + GingerUnits == TotalUnits)
model.addConstr(SulfateUnits <= MaxSulfateToGingerRatio * GingerUnits)


### Define the objective

model.setObjective(TimePerUnitSulfate * SulfateUnits + TimePerUnitGinger * GingerUnits, GRB.MINIMIZE)


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
