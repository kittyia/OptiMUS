
import os
import numpy as np
import json 
from gurobipy import Model, GRB, quicksum


model = Model("OptimizationProblem")

with open("data.json", "r") as f:
    data = json.load(f)




### Define the parameters

StaffShiftHours = data["StaffShiftHours"] # shape: [], definition: Number of hours worked per shift by a staff teacher

StaffShiftPay = data["StaffShiftPay"] # shape: [], definition: Payment per shift to a staff teacher

SubstituteShiftHours = data["SubstituteShiftHours"] # shape: [], definition: Number of hours worked per shift by a substitute teacher

SubstituteShiftPay = data["SubstituteShiftPay"] # shape: [], definition: Payment per shift to a substitute teacher

TotalTeachingHours = data["TotalTeachingHours"] # shape: [], definition: Total required teaching hours for the summer term

TotalBudget = data["TotalBudget"] # shape: [], definition: Total budget allocated for teacher payments



### Define the variables

StaffTeachers = model.addVar(vtype=GRB.INTEGER, name="StaffTeachers")

SubstituteTeachers = model.addVar(vtype=GRB.INTEGER, name="SubstituteTeachers")



### Define the constraints

model.addConstr(StaffShiftHours * StaffTeachers + SubstituteShiftHours * SubstituteTeachers >= TotalTeachingHours)
model.addConstr(StaffShiftPay * StaffTeachers + SubstituteShiftPay * SubstituteTeachers <= TotalBudget)
model.addConstr(StaffTeachers >= 0)
model.addConstr(SubstituteTeachers >= 0)
model.addConstr(StaffTeachers >= 0)
model.addConstr(SubstituteTeachers >= 0)


### Define the objective

model.setObjective(StaffTeachers + SubstituteTeachers, GRB.MINIMIZE)


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
