
import os
import numpy as np
import json 
from gurobipy import Model, GRB, quicksum


model = Model("OptimizationProblem")

with open("data.json", "r") as f:
    data = json.load(f)




### Define the parameters

NumFertilizers = data["NumFertilizers"] # shape: [], definition: Number of different fertilizers used in the compound

CostFertilizer = data["CostFertilizer"] # shape: ['NumFertilizers'], definition: Cost per kilogram of each fertilizer

NitrousOxidePerFertilizer = data["NitrousOxidePerFertilizer"] # shape: ['NumFertilizers'], definition: Units of nitrous oxide per kilogram of each fertilizer

VitaminMixPerFertilizer = data["VitaminMixPerFertilizer"] # shape: ['NumFertilizers'], definition: Units of vitamin mix per kilogram of each fertilizer

RequiredNitrousOxide = data["RequiredNitrousOxide"] # shape: [], definition: Minimum required units of nitrous oxide in the compound

RequiredVitaminMix = data["RequiredVitaminMix"] # shape: [], definition: Minimum required units of vitamin mix in the compound



### Define the variables

AmountFertilizer = model.addVars(NumFertilizers, vtype=GRB.CONTINUOUS, name="AmountFertilizer")



### Define the constraints

model.addConstr(
    sum(NitrousOxidePerFertilizer[i] * AmountFertilizer[i] for i in range(NumFertilizers)) 
    >= RequiredNitrousOxide
)
model.addConstr(
    sum(VitaminMixPerFertilizer[i] * AmountFertilizer[i] for i in range(NumFertilizers))
    >= RequiredVitaminMix
)
for i in range(NumFertilizers):
    model.addConstr(AmountFertilizer[i] >= 0)


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
