
import os
import numpy as np
import json 
from gurobipy import Model, GRB, quicksum


model = Model("OptimizationProblem")

with open("data.json", "r") as f:
    data = json.load(f)




### Define the parameters

EmployeesPerSmallTeam = data["EmployeesPerSmallTeam"] # shape: [], definition: Number of employees required per small team

AreaMowedSmallTeam = data["AreaMowedSmallTeam"] # shape: [], definition: Area mowed by a small team

EmployeesPerLargeTeam = data["EmployeesPerLargeTeam"] # shape: [], definition: Number of employees required per large team

AreaMowedLargeTeam = data["AreaMowedLargeTeam"] # shape: [], definition: Area mowed by a large team

TotalEmployees = data["TotalEmployees"] # shape: [], definition: Total number of employees available

RatioSmallToLargeTeams = data["RatioSmallToLargeTeams"] # shape: [], definition: Minimum ratio of small teams to large teams

MinLargeTeams = data["MinLargeTeams"] # shape: [], definition: Minimum number of large teams

MinSmallTeams = data["MinSmallTeams"] # shape: [], definition: Minimum number of small teams



### Define the variables

numberSmallTeams = model.addVar(vtype=GRB.INTEGER, name="numberSmallTeams")

numberLargeTeams = model.addVar(vtype=GRB.INTEGER, name="numberLargeTeams")



### Define the constraints

model.addConstr(
    EmployeesPerSmallTeam * numberSmallTeams +
    EmployeesPerLargeTeam * numberLargeTeams
    <= TotalEmployees
)
model.addConstr(numberSmallTeams >= RatioSmallToLargeTeams * numberLargeTeams)
model.addConstr(numberLargeTeams >= MinLargeTeams)
model.addConstr(numberSmallTeams >= 0)
model.addConstr(numberLargeTeams >= 0)


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
