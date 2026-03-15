
import os
import numpy as np
import json 
from gurobipy import Model, GRB, quicksum


model = Model("OptimizationProblem")

with open("data.json", "r") as f:
    data = json.load(f)




### Define the parameters

SeniorWage = data["SeniorWage"] # shape: [], definition: Weekly wage rate for senior citizens

YoungAdultWage = data["YoungAdultWage"] # shape: [], definition: Weekly wage rate for young adults

MaxWeeklyWageBill = data["MaxWeeklyWageBill"] # shape: [], definition: Maximum weekly wage bill

MinWorkersPerDay = data["MinWorkersPerDay"] # shape: [], definition: Minimum number of workers required per day

MinYoungAdultsPerDay = data["MinYoungAdultsPerDay"] # shape: [], definition: Minimum number of young adults required per day

MinYoungToSeniorRatio = data["MinYoungToSeniorRatio"] # shape: [], definition: Minimum ratio of young adults to senior citizens



### Define the variables

SeniorWorkers = model.addVar(vtype=GRB.INTEGER, name="SeniorWorkers")

YoungWorkers = model.addVar(vtype=GRB.INTEGER, name="YoungWorkers")



### Define the constraints

model.addConstr(SeniorWage * SeniorWorkers + YoungAdultWage * YoungWorkers <= MaxWeeklyWageBill)
model.addConstr(SeniorWorkers + YoungWorkers >= MinWorkersPerDay)
model.addConstr(YoungWorkers >= MinYoungToSeniorRatio * SeniorWorkers)
model.addConstr(SeniorWorkers >= 0)


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
