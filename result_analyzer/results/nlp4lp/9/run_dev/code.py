
import os
import numpy as np
import json 
from gurobipy import Model, GRB, quicksum


model = Model("OptimizationProblem")

with open("data.json", "r") as f:
    data = json.load(f)




### Define the parameters

NumJarTypes = data["NumJarTypes"] # shape: [], definition: Number of different types of terracotta jars produced

ShapingTimePerType = data["ShapingTimePerType"] # shape: ['NumJarTypes'], definition: Amount of shaping time required to produce one unit of each jar type

BakingTimePerType = data["BakingTimePerType"] # shape: ['NumJarTypes'], definition: Amount of baking time required to produce one unit of each jar type

ProfitPerType = data["ProfitPerType"] # shape: ['NumJarTypes'], definition: Profit earned per unit of each jar type

ShapingTimeAvailable = data["ShapingTimeAvailable"] # shape: [], definition: Total amount of shaping time available per week

BakingTimeAvailable = data["BakingTimeAvailable"] # shape: [], definition: Total amount of baking time available per week



### Define the variables

NumThinJars = model.addVar(vtype=GRB.INTEGER, name="NumThinJars")

NumStubbyJars = model.addVar(vtype=GRB.INTEGER, name="NumStubbyJars")



### Define the constraints

model.addConstr(90 * NumThinJars + 150 * NumStubbyJars <= BakingTimeAvailable)
model.addConstr(NumThinJars >= 0)
model.addConstr(NumStubbyJars >= 0)


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
