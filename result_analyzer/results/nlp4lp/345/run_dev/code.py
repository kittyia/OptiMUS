
import os
import numpy as np
import json 
from gurobipy import Model, GRB, quicksum


model = Model("OptimizationProblem")

with open("data.json", "r") as f:
    data = json.load(f)




### Define the parameters

NumMachines = data["NumMachines"] # shape: [], definition: Number of machines

NumParts = data["NumParts"] # shape: [], definition: Number of part types

TimeRequired = data["TimeRequired"] # shape: ['NumMachines', 'NumParts'], definition: Time required to produce one batch of part p on machine m

MachineCosts = data["MachineCosts"] # shape: ['NumMachines'], definition: Cost of operating machine m for one month

Availability = data["Availability"] # shape: ['NumMachines'], definition: Number of hours machine m is available each month without overtime

Prices = data["Prices"] # shape: ['NumParts'], definition: Price received for selling one batch of part p

MinBatches = data["MinBatches"] # shape: ['NumParts'], definition: Minimum number of batches of part p to be produced

StandardCost = data["StandardCost"] # shape: [], definition: Standard cost for operating all machines during normal operating hours

OvertimeCost = data["OvertimeCost"] # shape: [], definition: Extra cost for operating a machine in overtime per hour

OvertimeHour = data["OvertimeHour"] # shape: ['NumMachines'], definition: Number of overtime hours available for machine m



### Define the variables

batches = model.addVars(NumParts, vtype=GRB.CONTINUOUS, name="batches")

regularHours1 = model.addVar(vtype=GRB.CONTINUOUS, name="regularHours1")

overtimeHours1 = model.addVar(vtype=GRB.CONTINUOUS, name="overtimeHours1")



### Define the constraints

for m in range(1, NumMachines):
    model.addConstr(
        sum(TimeRequired[m][p] * batches[p] for p in range(NumParts)) 
        <= Availability[m]
    )
model.addConstr(
    regularHours1 + overtimeHours1 ==
    sum(TimeRequired[0][p] * batches[p] for p in range(NumParts))
)
model.addConstr(regularHours1 <= OvertimeHour[0])
for p in range(NumParts):
    model.addConstr(batches[p] >= MinBatches[p])
model.addConstr(regularHours1 >= 0)
model.addConstr(overtimeHours1 >= 0)


### Define the objective

model.setObjective(
    quicksum(Prices[p] * batches[p] for p in range(NumParts))
    - quicksum(
        MachineCosts[m] * quicksum(TimeRequired[m][p] * batches[p] for p in range(NumParts))
        for m in range(1, NumMachines)
    )
    - StandardCost * regularHours1
    - OvertimeCost * overtimeHours1,
    GRB.MAXIMIZE
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
