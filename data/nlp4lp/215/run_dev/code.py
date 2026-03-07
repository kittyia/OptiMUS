
import os
import numpy as np
import json 
from gurobipy import Model, GRB, quicksum


model = Model("OptimizationProblem")

with open("data.json", "r") as f:
    data = json.load(f)




### Define the parameters

WidePipeCapacity = data["WidePipeCapacity"] # shape: [], definition: Water transport capacity of a wide pipe (units per minute)

NarrowPipeCapacity = data["NarrowPipeCapacity"] # shape: [], definition: Water transport capacity of a narrow pipe (units per minute)

MaxWideToNarrowRatio = data["MaxWideToNarrowRatio"] # shape: [], definition: Maximum ratio of wide pipes to narrow pipes

MinTransportRequired = data["MinTransportRequired"] # shape: [], definition: Minimum required water transported per minute

MinWidePipes = data["MinWidePipes"] # shape: [], definition: Minimum number of wide pipes required



### Define the variables

WidePipes = model.addVar(vtype=GRB.INTEGER, name="WidePipes")

NarrowPipes = model.addVar(vtype=GRB.INTEGER, name="NarrowPipes")



### Define the constraints

model.addConstr(WidePipeCapacity * WidePipes + NarrowPipeCapacity * NarrowPipes >= MinTransportRequired)
model.addConstr(WidePipes <= MaxWideToNarrowRatio * NarrowPipes)
model.addConstr(WidePipes >= MinWidePipes)
model.addConstr(NarrowPipes >= 0)


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
