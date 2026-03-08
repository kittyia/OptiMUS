
import os
import numpy as np
import json 
from gurobipy import Model, GRB, quicksum


model = Model("OptimizationProblem")

with open("data.json", "r") as f:
    data = json.load(f)




### Define the parameters

NumDogTypes = data["NumDogTypes"] # shape: [], definition: Number of different dog types used in the school

NewspapersPerService = data["NewspapersPerService"] # shape: ['NumDogTypes'], definition: Number of newspapers delivered per service by each dog type

TreatsPerService = data["TreatsPerService"] # shape: ['NumDogTypes'], definition: Number of small bone treats required per service by each dog type

TotalBoneTreatsAvailable = data["TotalBoneTreatsAvailable"] # shape: [], definition: Total number of small bone treats available

MinGoldenRetrievers = data["MinGoldenRetrievers"] # shape: [], definition: Minimum number of golden retrievers to be used

MaxPercentageLabradors = data["MaxPercentageLabradors"] # shape: [], definition: Maximum percentage of dogs that can be labradors



### Define the variables

DogsUsed = model.addVars(NumDogTypes, vtype=GRB.INTEGER, name="DogsUsed")



### Define the constraints

model.addConstr(
    sum(TreatsPerService[i] * DogsUsed[i] for i in range(NumDogTypes))
    <= TotalBoneTreatsAvailable
)
model.addConstr(DogsUsed[2] >= MinGoldenRetrievers)
model.addConstr(
    DogsUsed[0] <= (MaxPercentageLabradors / 100.0) * 
    sum(DogsUsed[i] for i in range(NumDogTypes))
)
for i in range(NumDogTypes):
    model.addConstr(DogsUsed[i] >= 0)


### Define the objective

model.setObjective(quicksum(NewspapersPerService[i] * DogsUsed[i] 
                            for i in range(NumDogTypes)), 
                   GRB.MAXIMIZE)


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
