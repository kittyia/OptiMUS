
import os
import numpy as np
import json 
from gurobipy import Model, GRB, quicksum


model = Model("OptimizationProblem")

with open("data.json", "r") as f:
    data = json.load(f)




### Define the parameters

ManualSliceRate = data["ManualSliceRate"] # shape: [], definition: The number of slices a manual slicer can cut per minute

AutomaticSliceRate = data["AutomaticSliceRate"] # shape: [], definition: The number of slices an automatic slicer can cut per minute

ManualGreaseRate = data["ManualGreaseRate"] # shape: [], definition: The number of units of grease a manual slicer requires per minute

AutomaticGreaseRate = data["AutomaticGreaseRate"] # shape: [], definition: The number of units of grease an automatic slicer requires per minute

MinimumSlicesPerMinute = data["MinimumSlicesPerMinute"] # shape: [], definition: The minimum number of slices the shop needs to cut per minute

MaximumGreasePerMinute = data["MaximumGreasePerMinute"] # shape: [], definition: The maximum number of units of grease the shop can use per minute



### Define the variables

numberManualSlicers = model.addVar(vtype=GRB.INTEGER, name="numberManualSlicers")

numberAutomaticSlicers = model.addVar(vtype=GRB.INTEGER, name="numberAutomaticSlicers")



### Define the constraints

model.addConstr(ManualSliceRate * numberManualSlicers + AutomaticSliceRate * numberAutomaticSlicers >= MinimumSlicesPerMinute)
model.addConstr(ManualGreaseRate * numberManualSlicers + AutomaticGreaseRate * numberAutomaticSlicers <= MaximumGreasePerMinute)
model.addConstr(numberManualSlicers + 1 <= numberAutomaticSlicers)
model.addConstr(numberManualSlicers >= 0)
model.addConstr(numberAutomaticSlicers >= 0)


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
