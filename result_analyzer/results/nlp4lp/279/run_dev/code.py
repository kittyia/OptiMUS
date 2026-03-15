
import os
import numpy as np
import json 
from gurobipy import Model, GRB, quicksum


model = Model("OptimizationProblem")

with open("data.json", "r") as f:
    data = json.load(f)




### Define the parameters

K = data["K"] # shape: [], definition: Maximum value the random variable Z can take

ExpectedZ = data["ExpectedZ"] # shape: [], definition: Given expected value E[Z]

ExpectedZSquared = data["ExpectedZSquared"] # shape: [], definition: Given expected value E[Z^2]



### Define the variables

p = model.addVars(K+1, vtype=GRB.CONTINUOUS, name="p")



### Define the constraints

for k in range(K + 1):
    model.addConstr(p[k] >= 0)
model.addConstr(sum(p[k] for k in range(K + 1)) == 1)
model.addConstr(sum(k * p[k] for k in range(K + 1)) == ExpectedZ)
model.addConstr(sum(k * k * p[k] for k in range(K + 1)) == ExpectedZSquared)


### Define the objective

model.setObjective(quicksum((k**4) * p[k] for k in range(K+1)), GRB.MINIMIZE)


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
