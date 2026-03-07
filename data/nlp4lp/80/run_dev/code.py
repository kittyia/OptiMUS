
import os
import numpy as np
import json 
from gurobipy import Model, GRB, quicksum


model = Model("OptimizationProblem")

with open("data.json", "r") as f:
    data = json.load(f)




### Define the parameters

FullTimeHoursPerShift = data["FullTimeHoursPerShift"] # shape: [], definition: The number of hours a full time worker works per shift

PartTimeHoursPerShift = data["PartTimeHoursPerShift"] # shape: [], definition: The number of hours a part time worker works per shift

FullTimePayPerShift = data["FullTimePayPerShift"] # shape: [], definition: The amount paid to a full time worker per shift

PartTimePayPerShift = data["PartTimePayPerShift"] # shape: [], definition: The amount paid to a part time worker per shift

LaborHoursRequired = data["LaborHoursRequired"] # shape: [], definition: The total labor hours required for the project

TotalBudget = data["TotalBudget"] # shape: [], definition: The total budget available for labor costs



### Define the variables

FullTimeWorkers = model.addVar(vtype=GRB.INTEGER, name="FullTimeWorkers")

PartTimeWorkers = model.addVar(vtype=GRB.INTEGER, name="PartTimeWorkers")



### Define the constraints

model.addConstr(
    FullTimeHoursPerShift * FullTimeWorkers +
    PartTimeHoursPerShift * PartTimeWorkers
    >= LaborHoursRequired
)
model.addConstr(FullTimePayPerShift * FullTimeWorkers + PartTimePayPerShift * PartTimeWorkers <= TotalBudget)
model.addConstr(FullTimeWorkers >= 0)
model.addConstr(PartTimeWorkers >= 0)


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
