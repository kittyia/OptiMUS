
import os
import numpy as np
import json 
from gurobipy import Model, GRB, quicksum


model = Model("OptimizationProblem")

with open("data.json", "r") as f:
    data = json.load(f)




### Define the parameters

MetalAvailable = data["MetalAvailable"] # shape: [], definition: Total units of metal available

AcidAvailable = data["AcidAvailable"] # shape: [], definition: Total units of acid available

MaxHeat = data["MaxHeat"] # shape: [], definition: Maximum units of heat that can be given off

NumBoxTypes = data["NumBoxTypes"] # shape: [], definition: Number of different box types

MetalPerBoxType = data["MetalPerBoxType"] # shape: ['NumBoxTypes'], definition: Units of metal required per box type

AcidPerBoxType = data["AcidPerBoxType"] # shape: ['NumBoxTypes'], definition: Units of acid required per box type

FoamPerBoxType = data["FoamPerBoxType"] # shape: ['NumBoxTypes'], definition: Units of foam produced per box type

HeatPerBoxType = data["HeatPerBoxType"] # shape: ['NumBoxTypes'], definition: Units of heat given off per box type



### Define the variables

NumBoxes = model.addVars(NumBoxTypes, vtype=GRB.INTEGER, name="NumBoxes")



### Define the constraints

model.addConstr(
    sum(MetalPerBoxType[i] * NumBoxes[i] for i in range(NumBoxTypes)) <= MetalAvailable
)
model.addConstr(
    sum(AcidPerBoxType[i] * NumBoxes[i] for i in range(NumBoxTypes)) 
    <= AcidAvailable
)
model.addConstr(
    sum(HeatPerBoxType[i] * NumBoxes[i] for i in range(NumBoxTypes)) <= MaxHeat
)
for i in range(NumBoxTypes):
    model.addConstr(NumBoxes[i] >= 0)


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
