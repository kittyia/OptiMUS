
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

NumSetups = model.addVars(NumTables, vtype=GRB.INTEGER, name="NumSetups")



### Define the constraints

model.addConstr(sum(PowderUsed[i] * NumSetups[i] for i in range(NumTables)) <= AvailablePowder)
model.addConstr(sum(GlueUsed[i] * NumSetups[i] for i in range(NumTables)) <= AvailableGlue)
model.addConstr(
    sum(MessProduced[i] * NumSetups[i] for i in range(NumTables)) <= MaxMess
)
for i in range(NumTables):
    model.addConstr(NumSetups[i] >= 0)
# NumSetups[i] are defined as integer variables (vtype=GRB.INTEGER) when created,
# so no additional constraints are required to enforce integrality.


### Define the objective

model.setObjective(quicksum(SlimeProduced[i] * NumSetups[i] for i in range(NumTables)), GRB.MAXIMIZE)


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
