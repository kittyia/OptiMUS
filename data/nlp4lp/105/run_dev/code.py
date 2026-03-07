
import os
import numpy as np
import json 
from gurobipy import Model, GRB, quicksum


model = Model("OptimizationProblem")

with open("data.json", "r") as f:
    data = json.load(f)




### Define the parameters

TimePerFertilizer = data["TimePerFertilizer"] # shape: [], definition: Time one unit of fertilizer takes to be effective

TimePerSeeds = data["TimePerSeeds"] # shape: [], definition: Time one unit of seeds takes to be effective

MaxTotalUnits = data["MaxTotalUnits"] # shape: [], definition: Maximum total units of fertilizer and seeds combined

MinFertilizer = data["MinFertilizer"] # shape: [], definition: Minimum units of fertilizer to be added

MaxFertilizerRatio = data["MaxFertilizerRatio"] # shape: [], definition: Maximum ratio of fertilizer to seeds



### Define the variables

FertilizerUnits = model.addVar(vtype=GRB.CONTINUOUS, name="FertilizerUnits")

SeedsUnits = model.addVar(vtype=GRB.CONTINUOUS, name="SeedsUnits")



### Define the constraints

model.addConstr(FertilizerUnits + SeedsUnits <= MaxTotalUnits)
model.addConstr(FertilizerUnits >= MinFertilizer)
model.addConstr(FertilizerUnits <= MaxFertilizerRatio * SeedsUnits)


### Define the objective

del.setObjective(TimePerFertilizer * FertilizerUnits + TimePerSeeds * SeedsUnits, GRB.MINIMIZE


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
