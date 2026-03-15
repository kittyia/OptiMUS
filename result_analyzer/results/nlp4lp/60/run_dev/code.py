
import os
import numpy as np
import json 
from gurobipy import Model, GRB, quicksum


model = Model("OptimizationProblem")

with open("data.json", "r") as f:
    data = json.load(f)




### Define the parameters

NurseShiftHours = data["NurseShiftHours"] # shape: [], definition: Number of hours a nurse works per shift

PharmacistShiftHours = data["PharmacistShiftHours"] # shape: [], definition: Number of hours a pharmacist works per shift

NurseCostPerShift = data["NurseCostPerShift"] # shape: [], definition: Cost to employ one nurse per shift

PharmacistCostPerShift = data["PharmacistCostPerShift"] # shape: [], definition: Cost to employ one pharmacist per shift

TotalLaborHours = data["TotalLaborHours"] # shape: [], definition: Total required healthcare labor hours

TotalBudget = data["TotalBudget"] # shape: [], definition: Total budget for labor costs



### Define the variables

NurseShifts = model.addVar(vtype=GRB.INTEGER, name="NurseShifts")

PharmacistShifts = model.addVar(vtype=GRB.INTEGER, name="PharmacistShifts")



### Define the constraints

model.addConstr(NurseShiftHours * NurseShifts + PharmacistShiftHours * PharmacistShifts >= TotalLaborHours)
model.addConstr(NurseCostPerShift * NurseShifts + PharmacistCostPerShift * PharmacistShifts <= TotalBudget)
model.addConstr(NurseShifts >= 0)
model.addConstr(PharmacistShifts >= 0)


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
