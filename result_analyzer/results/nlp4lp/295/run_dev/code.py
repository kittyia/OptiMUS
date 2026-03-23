
import os
import numpy as np
import json 
from gurobipy import Model, GRB, quicksum


model = Model("OptimizationProblem")

with open("data.json", "r") as f:
    data = json.load(f)




### Define the parameters

ProbesPerSalinityTest = data["ProbesPerSalinityTest"] # shape: [], definition: Probes required per salinity test

ProbesPerPHTest = data["ProbesPerPHTest"] # shape: [], definition: Probes required per pH test

MinPHTests = data["MinPHTests"] # shape: [], definition: Minimum number of pH tests to be performed

MinTotalTests = data["MinTotalTests"] # shape: [], definition: Minimum total number of tests to be performed

MaxPHtoSalinityRatio = data["MaxPHtoSalinityRatio"] # shape: [], definition: Maximum ratio of number of pH tests to salinity tests



### Define the variables

PHTests = model.addVar(vtype=GRB.INTEGER, name="PHTests")

SalinityTests = model.addVar(vtype=GRB.INTEGER, name="SalinityTests")



### Define the constraints

model.addConstr(PHTests >= MinPHTests)
model.addConstr(PHTests + SalinityTests >= MinTotalTests)
model.addConstr(PHTests <= MaxPHtoSalinityRatio * SalinityTests)


### Define the objective

model.setObjective(
    ProbesPerSalinityTest * SalinityTests + ProbesPerPHTest * PHTests,
    GRB.MINIMIZE
)


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
