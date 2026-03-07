
import os
import numpy as np
import json 
from gurobipy import Model, GRB, quicksum


model = Model("OptimizationProblem")

with open("data.json", "r") as f:
    data = json.load(f)




### Define the parameters

NumShifts = data["NumShifts"] # shape: [], definition: Number of shifts for which officers are needed

OfficersNeeded = data["OfficersNeeded"] # shape: ['NumShifts'], definition: Number of officers needed for shift s

ShiftCosts = data["ShiftCosts"] # shape: ['NumShifts'], definition: Cost of assigning an officer to shift s



### Define the variables

officersAssigned = model.addVars(NumShifts, vtype=GRB.INTEGER, name="officersAssigned")



### Define the constraints

for s in range(NumShifts):
    model.addConstr(
        officersAssigned[s] + officersAssigned[(s - 1) % NumShifts] 
        >= OfficersNeeded[s]
    )
for s in range(NumShifts):
    model.addConstr(officersAssigned[s] >= 0)


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
