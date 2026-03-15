
import os
import numpy as np
import json 
from gurobipy import Model, GRB, quicksum


model = Model("OptimizationProblem")

with open("data.json", "r") as f:
    data = json.load(f)




### Define the parameters

K = data["K"] # shape: [], definition: Number of data points

ObservedValues = data["ObservedValues"] # shape: ['K'], definition: Observed y values at each data point k

ObservedXValues = data["ObservedXValues"] # shape: ['K'], definition: Observed x values at each data point k



### Define the variables

quadratic = model.addVar(vtype=GRB.CONTINUOUS, name="quadratic")

linear = model.addVar(vtype=GRB.CONTINUOUS, name="linear")

constant = model.addVar(vtype=GRB.CONTINUOUS, name="constant")

deviation = model.addVars(K, vtype=GRB.CONTINUOUS, name="deviation")



### Define the constraints

for k in range(K):
    model.addConstr(
        ObservedValues[k] - (
            quadratic * (ObservedXValues[k] ** 2)
            + linear * ObservedXValues[k]
            + constant
        ) <= deviation[k]
    )
for k in range(K):
    model.addConstr(
        -(ObservedValues[k] - (quadratic * ObservedXValues[k]**2 + linear * ObservedXValues[k] + constant))
        <= deviation[k]
    )


### Define the objective

model.setObjective(quicksum(deviation[k] for k in range(K)), GRB.MINIMIZE)


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
