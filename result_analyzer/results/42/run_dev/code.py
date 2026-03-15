
import os
import numpy as np
import json 
from gurobipy import Model, GRB, quicksum


model = Model("OptimizationProblem")

with open("data.json", "r") as f:
    data = json.load(f)




### Define the parameters

NumStoreTypes = data["NumStoreTypes"] # shape: [], definition: Number of types of stores available

SandwichesPerStoreType = data["SandwichesPerStoreType"] # shape: ['NumStoreTypes'], definition: Number of sandwiches produced per store type per day

EmployeesPerStoreType = data["EmployeesPerStoreType"] # shape: ['NumStoreTypes'], definition: Number of employees required per store type

MinimumSandwiches = data["MinimumSandwiches"] # shape: [], definition: Minimum number of sandwiches to be produced per day

MaximumEmployees = data["MaximumEmployees"] # shape: [], definition: Maximum number of employees available



### Define the variables

NumStores = model.addVars(NumStoreTypes, vtype=GRB.INTEGER, name="NumStores")



### Define the constraints

model.addConstr(
    sum(SandwichesPerStoreType[i] * NumStores[i] for i in range(NumStoreTypes)) 
    >= MinimumSandwiches
)
model.addConstr(
    sum(EmployeesPerStoreType[i] * NumStores[i] for i in range(NumStoreTypes))
    <= MaximumEmployees
)
for i in range(NumStoreTypes):
    model.addConstr(NumStores[i] >= 0)


### Define the objective

model.setObjective(quicksum(NumStores[i] for i in range(NumStoreTypes)), GRB.MINIMIZE)


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
