
import os
import numpy as np
import json 
from gurobipy import Model, GRB, quicksum


model = Model("OptimizationProblem")

with open("data.json", "r") as f:
    data = json.load(f)




### Define the parameters

TimeCoconutOil = data["TimeCoconutOil"] # shape: [], definition: Time taken for one unit of coconut oil to be effective

TimeLavender = data["TimeLavender"] # shape: [], definition: Time taken for one unit of lavender to be effective

MinCoconutOil = data["MinCoconutOil"] # shape: [], definition: Minimum required units of coconut oil

MaxTotalUnits = data["MaxTotalUnits"] # shape: [], definition: Maximum allowed units of both ingredients combined

MaxCoconutToLavenderRatio = data["MaxCoconutToLavenderRatio"] # shape: [], definition: Ratio constraint for the maximum units of coconut oil to lavender



### Define the variables

CoconutOilUnits = model.addVar(vtype=GRB.CONTINUOUS, name="CoconutOilUnits")

LavenderUnits = model.addVar(vtype=GRB.CONTINUOUS, name="LavenderUnits")



### Define the constraints

model.addConstr(CoconutOilUnits >= MinCoconutOil)
model.addConstr(CoconutOilUnits + LavenderUnits <= MaxTotalUnits)
model.addConstr(CoconutOilUnits <= MaxCoconutToLavenderRatio * LavenderUnits)


### Define the objective

model.setObjective(TimeCoconutOil * CoconutOilUnits + TimeLavender * LavenderUnits, GRB.MINIMIZE)


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
