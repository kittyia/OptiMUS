
import os
import numpy as np
import json 
from gurobipy import Model, GRB, quicksum


model = Model("OptimizationProblem")

with open("data.json", "r") as f:
    data = json.load(f)




### Define the parameters

GlassJarCapacity = data["GlassJarCapacity"] # shape: [], definition: The capacity of a glass jar in milliliters

PlasticJarCapacity = data["PlasticJarCapacity"] # shape: [], definition: The capacity of a plastic jar in milliliters

MinPlasticToGlassRatio = data["MinPlasticToGlassRatio"] # shape: [], definition: The minimum ratio of plastic jars to glass jars that must be filled

MinNumberGlassJars = data["MinNumberGlassJars"] # shape: [], definition: The minimum number of glass jars that must be filled

TotalHoney = data["TotalHoney"] # shape: [], definition: Total amount of honey available in milliliters



### Define the variables

GlassJars = model.addVar(vtype=GRB.INTEGER, name="GlassJars")

PlasticJars = model.addVar(vtype=GRB.INTEGER, name="PlasticJars")



### Define the constraints

model.addConstr(GlassJarCapacity * GlassJars + PlasticJarCapacity * PlasticJars <= TotalHoney)
model.addConstr(PlasticJars >= MinPlasticToGlassRatio * GlassJars)
model.addConstr(GlassJars >= MinNumberGlassJars)
GlassJars.vtype = GRB.INTEGER
PlasticJars.vtype = GRB.INTEGER


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
