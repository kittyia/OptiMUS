
import os
import numpy as np
import json 
from gurobipy import Model, GRB, quicksum


model = Model("OptimizationProblem")

with open("data.json", "r") as f:
    data = json.load(f)




### Define the parameters

NumSegments = data["NumSegments"] # shape: [], definition: Number of road segments

NumLamps = data["NumLamps"] # shape: [], definition: Number of lamps

Coefficients = data["Coefficients"] # shape: ['NumSegments', 'NumLamps'], definition: Coefficient showing how much illumination segment i gets from lamp j

DesiredIlluminations = data["DesiredIlluminations"] # shape: ['NumSegments'], definition: Desired illumination level for each segment



### Define the variables

LampPower = model.addVars(NumLamps, vtype=GRB.CONTINUOUS, name="LampPower")



### Define the constraints

for j in range(NumLamps):
    model.addConstr(LampPower[j] >= 0)


### Define the objective

model.setObjective(
    quicksum(
        abs_(
            quicksum(Coefficients[i][j] * LampPower[j] for j in range(NumLamps))
            - DesiredIlluminations[i]
        )
        for i in range(NumSegments)
    ),
    GRB.MINIMIZE
)


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
