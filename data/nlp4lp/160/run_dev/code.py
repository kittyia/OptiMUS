
import os
import numpy as np
import json 
from gurobipy import Model, GRB, quicksum


model = Model("OptimizationProblem")

with open("data.json", "r") as f:
    data = json.load(f)




### Define the parameters

SmallSuitcaseCapacity = data["SmallSuitcaseCapacity"] # shape: [], definition: Capacity of a small suitcase in snacks

LargeSuitcaseCapacity = data["LargeSuitcaseCapacity"] # shape: [], definition: Capacity of a large suitcase in snacks

MinSmallToLargeRatio = data["MinSmallToLargeRatio"] # shape: [], definition: Minimum ratio factor indicating that the number of small suitcases must be at least twice the number of large suitcases

MaxSmallSuitcases = data["MaxSmallSuitcases"] # shape: [], definition: Maximum number of small suitcases available

MaxLargeSuitcases = data["MaxLargeSuitcases"] # shape: [], definition: Maximum number of large suitcases available

MinLargeSuitcases = data["MinLargeSuitcases"] # shape: [], definition: Minimum number of large suitcases to send

MaxTotalSuitcases = data["MaxTotalSuitcases"] # shape: [], definition: Maximum total number of suitcases to send



### Define the variables

SmallSuitcases = model.addVar(vtype=GRB.INTEGER, name="SmallSuitcases")

LargeSuitcases = model.addVar(vtype=GRB.INTEGER, name="LargeSuitcases")



### Define the constraints

model.addConstr(SmallSuitcases >= MinSmallToLargeRatio * LargeSuitcases)
model.addConstr(LargeSuitcases >= MinLargeSuitcases)
model.addConstr(SmallSuitcases + LargeSuitcases <= MaxTotalSuitcases)


### Define the objective

del.setObjective(SmallSuitcaseCapacity * SmallSuitcases + LargeSuitcaseCapacity * LargeSuitcases, GRB.MAXIMIZE


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
