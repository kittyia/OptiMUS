
import os
import numpy as np
import json 
from gurobipy import Model, GRB, quicksum


model = Model("OptimizationProblem")

with open("data.json", "r") as f:
    data = json.load(f)




### Define the parameters

WorkersPerSmallBin = data["WorkersPerSmallBin"] # shape: [], definition: Number of workers required for a small bin

WorkersPerLargeBin = data["WorkersPerLargeBin"] # shape: [], definition: Number of workers required for a large bin

CapacitySmallBin = data["CapacitySmallBin"] # shape: [], definition: Capacity of a small bin in units of recycling material

CapacityLargeBin = data["CapacityLargeBin"] # shape: [], definition: Capacity of a large bin in units of recycling material

TotalWorkers = data["TotalWorkers"] # shape: [], definition: Total number of available workers

SmallBinToLargeBinRatio = data["SmallBinToLargeBinRatio"] # shape: [], definition: Required ratio of small bins to large bins

MinimumSmallBins = data["MinimumSmallBins"] # shape: [], definition: Minimum number of small bins

MinimumLargeBins = data["MinimumLargeBins"] # shape: [], definition: Minimum number of large bins



### Define the variables

SmallBins = model.addVar(vtype=GRB.INTEGER, name="SmallBins")

LargeBins = model.addVar(vtype=GRB.INTEGER, name="LargeBins")



### Define the constraints

model.addConstr(WorkersPerSmallBin * SmallBins + WorkersPerLargeBin * LargeBins <= TotalWorkers)
model.addConstr(SmallBins == SmallBinToLargeBinRatio * LargeBins)
model.addConstr(LargeBins >= MinimumLargeBins)
model.addConstr(SmallBins >= 0)
model.addConstr(LargeBins >= 0)


### Define the objective

model.setObjective(CapacitySmallBin * SmallBins + CapacityLargeBin * LargeBins, GRB.MAXIMIZE)


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
