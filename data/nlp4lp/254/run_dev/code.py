
import os
import numpy as np
import json 
from gurobipy import Model, GRB, quicksum


model = Model("OptimizationProblem")

with open("data.json", "r") as f:
    data = json.load(f)




### Define the parameters

SpecializedAnnotRate = data["SpecializedAnnotRate"] # shape: [], definition: Annotation rate of the specialized company (images per hour)

CommonAnnotRate = data["CommonAnnotRate"] # shape: [], definition: Annotation rate of the common company (images per hour)

SpecializedCostPerHour = data["SpecializedCostPerHour"] # shape: [], definition: Cost per hour of the specialized company

CommonCostPerHour = data["CommonCostPerHour"] # shape: [], definition: Cost per hour of the common company

MinTotalImages = data["MinTotalImages"] # shape: [], definition: Minimum number of images to annotate

MinSpecializedFraction = data["MinSpecializedFraction"] # shape: [], definition: Minimum fraction of work allocated to the specialized company



### Define the variables

SpecializedHours = model.addVar(vtype=GRB.CONTINUOUS, name="SpecializedHours")

CommonHours = model.addVar(vtype=GRB.CONTINUOUS, name="CommonHours")

SpecializedImages = model.addVar(vtype=GRB.CONTINUOUS, name="SpecializedImages")

CommonImages = model.addVar(vtype=GRB.CONTINUOUS, name="CommonImages")



### Define the constraints

model.addConstr(
    SpecializedAnnotRate * SpecializedHours + 
    CommonAnnotRate * CommonHours 
    >= MinTotalImages
)
model.addConstr(
    SpecializedAnnotRate * SpecializedHours
    >= MinSpecializedFraction * (
        SpecializedAnnotRate * SpecializedHours
        + CommonAnnotRate * CommonHours
    )
)
model.addConstr(SpecializedImages == SpecializedAnnotRate * SpecializedHours)
model.addConstr(CommonImages == CommonAnnotRate * CommonHours)
model.addConstr(SpecializedHours >= 0)
model.addConstr(CommonHours >= 0)


### Define the objective

model.setObjective(SpecializedCostPerHour * SpecializedHours + CommonCostPerHour * CommonHours, GRB.MINIMIZE)


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
