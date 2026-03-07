
import os
import numpy as np
import json 
from gurobipy import Model, GRB, quicksum


model = Model("OptimizationProblem")

with open("data.json", "r") as f:
    data = json.load(f)




### Define the parameters

NumMixes = data["NumMixes"] # shape: [], definition: Number of different candy mixes prepared

NumCandyTypes = data["NumCandyTypes"] # shape: [], definition: Number of different candy types used

CompositionRequired = data["CompositionRequired"] # shape: ['NumCandyTypes', 'NumMixes'], definition: Amount of each candy type required per kilogram of each mix

ProfitPerMix = data["ProfitPerMix"] # shape: ['NumMixes'], definition: Profit per kilogram of each mix

AvailableCandy = data["AvailableCandy"] # shape: ['NumCandyTypes'], definition: Amount of each candy type available



### Define the variables

MixProduced = model.addVars(NumMixes, vtype=GRB.CONTINUOUS, name="MixProduced")



### Define the constraints

model.addConstr(0.8 * MixProduced[0] + 0.1 * MixProduced[1] <= 80)
model.addConstr(0.2 * MixProduced[0] + 0.9 * MixProduced[1] <= 60)
for m in range(NumMixes):
    model.addConstr(MixProduced[m] >= 0)


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
