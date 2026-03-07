
import os
import numpy as np
import json 
from gurobipy import Model, GRB, quicksum


model = Model("OptimizationProblem")

with open("data.json", "r") as f:
    data = json.load(f)




### Define the parameters

TimeSpitTest = data["TimeSpitTest"] # shape: [], definition: Time to administer a spit test

TimeSwabTest = data["TimeSwabTest"] # shape: [], definition: Time to administer a swab test

MinRatioSpitToSwab = data["MinRatioSpitToSwab"] # shape: [], definition: Minimum ratio of spit tests to swab tests

MinSwabTests = data["MinSwabTests"] # shape: [], definition: Minimum number of swab tests to administer

TotalOperatingTime = data["TotalOperatingTime"] # shape: [], definition: Total operating time in minutes



### Define the variables

SpitTests = model.addVar(vtype=GRB.INTEGER, name="SpitTests")

SwabTests = model.addVar(vtype=GRB.INTEGER, name="SwabTests")



### Define the constraints

model.addConstr(TimeSpitTest * SpitTests + TimeSwabTest * SwabTests <= TotalOperatingTime)
model.addConstr(SpitTests >= MinRatioSpitToSwab * SwabTests)
model.addConstr(SwabTests >= MinSwabTests)


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
