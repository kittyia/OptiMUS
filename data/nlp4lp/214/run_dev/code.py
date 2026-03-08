
import os
import numpy as np
import json 
from gurobipy import Model, GRB, quicksum


model = Model("OptimizationProblem")

with open("data.json", "r") as f:
    data = json.load(f)




### Define the parameters

TimeTemperatureCheck = data["TimeTemperatureCheck"] # shape: [], definition: Time taken to perform a temperature check

TimeBloodTest = data["TimeBloodTest"] # shape: [], definition: Time taken to perform a blood test

MinBloodTests = data["MinBloodTests"] # shape: [], definition: Minimum number of blood tests required

TempToBloodRatio = data["TempToBloodRatio"] # shape: [], definition: Minimum ratio of temperature checks to blood tests

TotalStaffMinutes = data["TotalStaffMinutes"] # shape: [], definition: Total staff minutes available



### Define the variables

NumTemperatureChecks = model.addVar(vtype=GRB.INTEGER, name="NumTemperatureChecks")

NumBloodTests = model.addVar(vtype=GRB.INTEGER, name="NumBloodTests")



### Define the constraints

model.addConstr(TimeTemperatureCheck * NumTemperatureChecks + TimeBloodTest * NumBloodTests <= TotalStaffMinutes)
model.addConstr(NumBloodTests >= MinBloodTests)
model.addConstr(NumTemperatureChecks >= TempToBloodRatio * NumBloodTests)


### Define the objective

model.setObjective(NumTemperatureChecks + NumBloodTests, GRB.MAXIMIZE)


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
