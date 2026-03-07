
import os
import numpy as np
import json 
from gurobipy import Model, GRB, quicksum


model = Model("OptimizationProblem")

with open("data.json", "r") as f:
    data = json.load(f)




### Define the parameters

NumTables = data["NumTables"] # shape: [], definition: Number of different tables for making slime

PowderUsed = data["PowderUsed"] # shape: ['NumTables'], definition: Amount of powder used by table i

GlueUsed = data["GlueUsed"] # shape: ['NumTables'], definition: Amount of glue used by table i

SlimeProduced = data["SlimeProduced"] # shape: ['NumTables'], definition: Amount of slime produced by table i

MessProduced = data["MessProduced"] # shape: ['NumTables'], definition: Amount of mess produced by table i

AvailablePowder = data["AvailablePowder"] # shape: [], definition: Total available units of powder

AvailableGlue = data["AvailableGlue"] # shape: [], definition: Total available units of glue

MaxMess = data["MaxMess"] # shape: [], definition: Maximum allowable units of mess



### Define the variables

TablesSetup = model.addVars(NumTables, vtype=GRB.INTEGER, name="TablesSetup")



### Define the constraints

model.addConstr(sum(GlueUsed[i] * TablesSetup[i] for i in range(NumTables)) <= AvailableGlue)
model.addConstr(
    sum(MessProduced[i] * TablesSetup[i] for i in range(NumTables)) <= MaxMess
)
model.addConstr(TablesSetup[0] >= 0)
model.addConstr(TablesSetup[1] >= 0)
for i in range(NumTables):
    model.addConstr(TablesSetup[i] >= 0)


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
