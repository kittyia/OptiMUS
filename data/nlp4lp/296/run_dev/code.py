
import os
import numpy as np
import json 
from gurobipy import Model, GRB, quicksum


model = Model("OptimizationProblem")

with open("data.json", "r") as f:
    data = json.load(f)




### Define the parameters

PartTimeHours = data["PartTimeHours"] # shape: [], definition: Part-time staff weekly working hours

PartTimeWage = data["PartTimeWage"] # shape: [], definition: Part-time staff weekly wage

FullTimeHours = data["FullTimeHours"] # shape: [], definition: Full-time staff weekly working hours

FullTimeWage = data["FullTimeWage"] # shape: [], definition: Full-time staff weekly wage

TotalHoursRequired = data["TotalHoursRequired"] # shape: [], definition: Total weekly working hours required

TotalBudget = data["TotalBudget"] # shape: [], definition: Total budget for mail delivery



### Define the variables

PartTimeStaff = model.addVar(vtype=GRB.INTEGER, name="PartTimeStaff")

FullTimeStaff = model.addVar(vtype=GRB.INTEGER, name="FullTimeStaff")



### Define the constraints

model.addConstr(PartTimeHours * PartTimeStaff + FullTimeHours * FullTimeStaff >= TotalHoursRequired)
model.addConstr(PartTimeWage * PartTimeStaff + FullTimeWage * FullTimeStaff <= TotalBudget)
model.addConstr(PartTimeStaff >= 0)
model.addConstr(FullTimeStaff >= 0)


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
