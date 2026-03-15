
import os
import numpy as np
import json 
from gurobipy import Model, GRB, quicksum


model = Model("OptimizationProblem")

with open("data.json", "r") as f:
    data = json.load(f)




### Define the parameters

SmallJarCapacity = data["SmallJarCapacity"] # shape: [], definition: Capacity of a small jar in milliliters

LargeJarCapacity = data["LargeJarCapacity"] # shape: [], definition: Capacity of a large jar in milliliters

MinJamVolume = data["MinJamVolume"] # shape: [], definition: Minimum total volume of jam to ship in milliliters

MaxLargeJarsRatio = data["MaxLargeJarsRatio"] # shape: [], definition: Maximum allowed ratio of large jars to small jars



### Define the variables

NumberOfSmallJars = model.addVar(vtype=GRB.INTEGER, name="NumberOfSmallJars")

NumberOfLargeJars = model.addVar(vtype=GRB.INTEGER, name="NumberOfLargeJars")



### Define the constraints

model.addConstr(
    SmallJarCapacity * NumberOfSmallJars + 
    LargeJarCapacity * NumberOfLargeJars 
    >= MinJamVolume
)
model.addConstr(NumberOfLargeJars <= NumberOfSmallJars)
model.addConstr(NumberOfSmallJars >= 0)
model.addConstr(NumberOfLargeJars >= 0)


### Define the objective

model.setObjective(NumberOfSmallJars + NumberOfLargeJars, GRB.MINIMIZE)


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
