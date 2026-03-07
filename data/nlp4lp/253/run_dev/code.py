
import os
import numpy as np
import json 
from gurobipy import Model, GRB, quicksum


model = Model("OptimizationProblem")

with open("data.json", "r") as f:
    data = json.load(f)




### Define the parameters

TimePerBloodTest = data["TimePerBloodTest"] # shape: [], definition: Time required to perform a blood test in minutes

TimePerEarTest = data["TimePerEarTest"] # shape: [], definition: Time required to perform an ear test in minutes

BloodToEarTestRatio = data["BloodToEarTestRatio"] # shape: [], definition: Minimum ratio of blood tests to ear tests

MinEarTests = data["MinEarTests"] # shape: [], definition: Minimum number of ear tests to be administered

TotalOperatingTime = data["TotalOperatingTime"] # shape: [], definition: Total operating time of the clinic in minutes



### Define the variables

BloodTests = model.addVar(vtype=GRB.INTEGER, name="BloodTests")

EarTests = model.addVar(vtype=GRB.INTEGER, name="EarTests")



### Define the constraints

model.addConstr(TimePerBloodTest * BloodTests + TimePerEarTest * EarTests <= TotalOperatingTime)
model.addConstr(BloodTests >= BloodToEarTestRatio * EarTests)
model.addConstr(EarTests >= MinEarTests)


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
