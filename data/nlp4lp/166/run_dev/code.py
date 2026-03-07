
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

smallJars = model.addVar(vtype=GRB.INTEGER, name="smallJars")

largeJars = model.addVar(vtype=GRB.INTEGER, name="largeJars")



### Define the constraints

model.addConstr(SmallJarCapacity * smallJars + LargeJarCapacity * largeJars >= MinJamVolume)
model.addConstr(largeJars <= MaxLargeJarsRatio * smallJars)
model.addConstr(smallJars >= 0)
model.addConstr(largeJars >= 0)


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
