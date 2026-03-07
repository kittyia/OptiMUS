
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

coconutOilUnits = model.addVar(vtype=GRB.CONTINUOUS, name="coconutOilUnits")

lavenderUnits = model.addVar(vtype=GRB.CONTINUOUS, name="lavenderUnits")



### Define the constraints

model.addConstr(coconutOilUnits >= MinCoconutOil)
model.addConstr(coconutOilUnits + lavenderUnits <= MaxTotalUnits)
model.addConstr(coconutOilUnits <= MaxCoconutToLavenderRatio * lavenderUnits)


### Define the objective

model.setObjective(TimeCoconutOil * coconutOilUnits + TimeLavender * lavenderUnits, GRB.MINIMIZE)


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
