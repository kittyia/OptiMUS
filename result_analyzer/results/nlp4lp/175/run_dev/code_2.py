import os
import numpy as np
import json
from gurobipy import Model, GRB, quicksum

model = Model("OptimizationProblem")

with open("data.json", "r") as f:
    data = json.load(f)

### Define the parameters

NumDogTypes = data["NumDogTypes"]  # Number of different dog types
NewspapersPerService = data["NewspapersPerService"]
TreatsPerService = data["TreatsPerService"]
TotalBoneTreatsAvailable = data["TotalBoneTreatsAvailable"]
MinGoldenRetrievers = data["MinGoldenRetrievers"]
MaxPercentageLabradors = data["MaxPercentageLabradors"]

### Define the variables

DogsUsed = model.addVars(NumDogTypes, vtype=GRB.INTEGER, name="DogsUsed")

### Define the constraints

# Treat constraint
model.addConstr(
    quicksum(TreatsPerService[i] * DogsUsed[i] for i in range(NumDogTypes))
    <= TotalBoneTreatsAvailable
)

# Golden retrievers minimum (index 1 assumed to be golden retrievers)
model.addConstr(DogsUsed[1] >= MinGoldenRetrievers)

# Maximum percentage of labradors (index 0 assumed to be labradors)
model.addConstr(
    DogsUsed[0] <= (MaxPercentageLabradors / 100.0) *
    quicksum(DogsUsed[i] for i in range(NumDogTypes))
)

# Non-negativity (redundant but explicit)
for i in range(NumDogTypes):
    model.addConstr(DogsUsed[i] >= 0)

### Define the objective

model.setObjective(
    quicksum(NewspapersPerService[i] * DogsUsed[i]
             for i in range(NumDogTypes)),
    GRB.MAXIMIZE
)

### Optimize the model

model.optimize()

### Output optimal objective value

if model.status == GRB.OPTIMAL:
    print("Optimal Objective Value: ", model.objVal)
    with open("output_solution.txt", "w") as f:
        f.write(str(model.objVal))
else:
    with open("output_solution.txt", "w") as f:
        f.write(str(model.status))