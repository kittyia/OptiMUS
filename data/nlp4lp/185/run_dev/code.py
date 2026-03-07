
import os
import numpy as np
import json 
from gurobipy import Model, GRB, quicksum


model = Model("OptimizationProblem")

with open("data.json", "r") as f:
    data = json.load(f)




### Define the parameters

PigeonLetterCapacity = data["PigeonLetterCapacity"] # shape: [], definition: The number of letters a carrier pigeon can carry at a time

PigeonTreatCost = data["PigeonTreatCost"] # shape: [], definition: The number of treats required for a carrier pigeon's service

OwlLetterCapacity = data["OwlLetterCapacity"] # shape: [], definition: The number of letters an owl can carry at a time

OwlTreatCost = data["OwlTreatCost"] # shape: [], definition: The number of treats required for an owl's service

MaxOwlProportion = data["MaxOwlProportion"] # shape: [], definition: The maximum proportion of birds that can be owls

TotalTreats = data["TotalTreats"] # shape: [], definition: The total number of treats available

MinPigeons = data["MinPigeons"] # shape: [], definition: The minimum number of carrier pigeons that must be used



### Define the variables

Pigeons = model.addVar(vtype=GRB.INTEGER, name="Pigeons")

Owls = model.addVar(vtype=GRB.INTEGER, name="Owls")



### Define the constraints

model.addConstr(PigeonTreatCost * Pigeons + OwlTreatCost * Owls <= TotalTreats)
model.addConstr(3 * Owls <= 2 * Pigeons)
model.addConstr(Pigeons >= MinPigeons)
model.addConstr(Owls >= 0)


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
