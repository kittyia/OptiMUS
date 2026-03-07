
import os
import numpy as np
import json 
from gurobipy import Model, GRB, quicksum


model = Model("OptimizationProblem")

with open("data.json", "r") as f:
    data = json.load(f)




### Define the parameters

SeniorWage = data["SeniorWage"] # shape: [], definition: Weekly wage of a senior accountant

JuniorWage = data["JuniorWage"] # shape: [], definition: Weekly wage of a junior accountant

MinTotalAccountants = data["MinTotalAccountants"] # shape: [], definition: Minimum total number of accountants required

MinSeniorAccountants = data["MinSeniorAccountants"] # shape: [], definition: Minimum number of senior accountants required

SeniorToJuniorRatio = data["SeniorToJuniorRatio"] # shape: [], definition: Minimum ratio of senior to junior accountants

WageBillLimit = data["WageBillLimit"] # shape: [], definition: Maximum weekly wage bill



### Define the variables

SeniorAccountants = model.addVar(vtype=GRB.INTEGER, name="SeniorAccountants")

JuniorAccountants = model.addVar(vtype=GRB.INTEGER, name="JuniorAccountants")



### Define the constraints

model.addConstr(SeniorAccountants + JuniorAccountants >= MinTotalAccountants)
model.addConstr(SeniorAccountants >= MinSeniorAccountants)
model.addConstr(SeniorAccountants >= SeniorToJuniorRatio * JuniorAccountants)
model.addConstr(SeniorWage * SeniorAccountants + JuniorWage * JuniorAccountants <= WageBillLimit)
model.addConstr(SeniorAccountants >= 0)
model.addConstr(JuniorAccountants >= 0)


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
