import os
import numpy as np
import json
from gurobipy import Model, GRB, quicksum


model = Model("OptimizationProblem")

with open("data.json", "r") as f:
    data = json.load(f)


### Define the parameters

SmallSuitcaseCapacity = data["SmallSuitcaseCapacity"]
LargeSuitcaseCapacity = data["LargeSuitcaseCapacity"]
MinSmallToLargeRatio = data["MinSmallToLargeRatio"]
MaxSmallSuitcases = data["MaxSmallSuitcases"]
MaxLargeSuitcases = data["MaxLargeSuitcases"]
MinLargeSuitcases = data["MinLargeSuitcases"]
MaxTotalSuitcases = data["MaxTotalSuitcases"]


### Define the variables

SmallSuitcases = model.addVar(vtype=GRB.INTEGER, lb=0, name="SmallSuitcases")
LargeSuitcases = model.addVar(vtype=GRB.INTEGER, lb=0, name="LargeSuitcases")


### Define the constraints

model.addConstr(SmallSuitcases >= MinSmallToLargeRatio * LargeSuitcases)
model.addConstr(LargeSuitcases >= MinLargeSuitcases)
model.addConstr(SmallSuitcases <= MaxSmallSuitcases)
model.addConstr(LargeSuitcases <= MaxLargeSuitcases)
model.addConstr(SmallSuitcases + LargeSuitcases <= MaxTotalSuitcases)


### Define the objective

model.setObjective(
    SmallSuitcaseCapacity * SmallSuitcases +
    LargeSuitcaseCapacity * LargeSuitcases,
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