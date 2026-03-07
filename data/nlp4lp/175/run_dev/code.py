
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

NumLabradors = model.addVar(vtype=GRB.INTEGER, name="NumLabradors")

NumGoldenRetrievers = model.addVar(vtype=GRB.INTEGER, name="NumGoldenRetrievers")



### Define the constraints

model.addConstr(5 * NumLabradors + 6 * NumGoldenRetrievers <= TotalBoneTreatsAvailable)
model.addConstr(NumGoldenRetrievers >= MinGoldenRetrievers)
model.addConstr(NumLabradors <= (MaxPercentageLabradors / 100.0) * (NumLabradors + NumGoldenRetrievers))
model.addConstr(NumLabradors >= 0)
model.addConstr(NumLabradors >= 0)
model.addConstr(NumGoldenRetrievers >= 0)


### Define the objective

model.setObjective(7 * NumLabradors + 10 * NumGoldenRetrievers, GRB.MAXIMIZE)


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
