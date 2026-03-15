
import os
import numpy as np
import json 
from gurobipy import Model, GRB, quicksum


model = Model("OptimizationProblem")

with open("data.json", "r") as f:
    data = json.load(f)




### Define the parameters

AssemblyTimeDesk = data["AssemblyTimeDesk"] # shape: [], definition: Minutes required for assembly per desk

SandingTimeDesk = data["SandingTimeDesk"] # shape: [], definition: Minutes required for sanding per desk

AssemblyTimeDrawer = data["AssemblyTimeDrawer"] # shape: [], definition: Minutes required for assembly per drawer

SandingTimeDrawer = data["SandingTimeDrawer"] # shape: [], definition: Minutes required for sanding per drawer

TotalAssemblyTime = data["TotalAssemblyTime"] # shape: [], definition: Total available assembly minutes

TotalSandingTime = data["TotalSandingTime"] # shape: [], definition: Total available sanding minutes

ProfitPerDesk = data["ProfitPerDesk"] # shape: [], definition: Profit per desk

ProfitPerDrawer = data["ProfitPerDrawer"] # shape: [], definition: Profit per drawer



### Define the variables

NumDesks = model.addVar(vtype=GRB.INTEGER, name="NumDesks")

NumDrawers = model.addVar(vtype=GRB.INTEGER, name="NumDrawers")



### Define the constraints

model.addConstr(AssemblyTimeDesk * NumDesks + AssemblyTimeDrawer * NumDrawers <= TotalAssemblyTime)
model.addConstr(NumDesks >= 0)
model.addConstr(NumDrawers >= 0)
model.addConstr(NumDesks >= 0)
model.addConstr(NumDrawers >= 0)


### Define the objective

model.setObjective(ProfitPerDesk * NumDesks + ProfitPerDrawer * NumDrawers, GRB.MAXIMIZE)


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
