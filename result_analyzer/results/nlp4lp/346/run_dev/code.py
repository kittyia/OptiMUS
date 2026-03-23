
import os
import numpy as np
import json 
from gurobipy import Model, GRB, quicksum


model = Model("OptimizationProblem")

with open("data.json", "r") as f:
    data = json.load(f)




### Define the parameters

M = data["M"] # shape: [], definition: Number of machines

P = data["P"] # shape: [], definition: Number of parts to be produced

TimeRequired = data["TimeRequired"] # shape: ['M', 'P'], definition: Time required to produce each part 'p' on machine 'm'

MachineCosts = data["MachineCosts"] # shape: ['M'], definition: Cost associated with each machine 'm'

Availability = data["Availability"] # shape: ['M'], definition: Availability in hours of each machine 'm' per month

Prices = data["Prices"] # shape: ['P'], definition: Price obtained from selling each part 'p'

MinBatches = data["MinBatches"] # shape: ['P'], definition: Minimum number of batches of part 'p' that must be produced

StandardCost = data["StandardCost"] # shape: [], definition: Standard cost for a machine to run for one hour

OvertimeCost = data["OvertimeCost"] # shape: [], definition: Overtime cost for a machine to run for one hour beyond the standard availability

OvertimeHour = data["OvertimeHour"] # shape: [], definition: Numbers of overtime hours available for a machine to run beyond standard availability

MinProfit = data["MinProfit"] # shape: [], definition: The minimum profit the manufacturer wants to achieve



### Define the variables

standardHours = model.addVar(vtype=GRB.CONTINUOUS, name="standardHours")

overtimeHours = model.addVar(vtype=GRB.CONTINUOUS, name="overtimeHours")

batches = model.addVars(P, vtype=GRB.CONTINUOUS, name="batches")



### Define the constraints

for m in range(1, M):  
    model.addConstr(  
        sum(TimeRequired[m][p] * batches[p] for p in range(P))  
        <= Availability[m]  
    )
model.addConstr(
    sum(TimeRequired[0][p] * batches[p] for p in range(P)) 
    == standardHours + overtimeHours
)
model.addConstr(standardHours <= OvertimeHour)
model.addConstr(standardHours >= 0)
model.addConstr(overtimeHours >= 0)
for p in range(P):
    model.addConstr(batches[p] >= MinBatches[p])
model.addConstr(
    sum(Prices[p] * batches[p] for p in range(P))
    - (
        sum(
            MachineCosts[m] * sum(TimeRequired[m][p] * batches[p] for p in range(P))
            for m in range(1, M)
        )
        + StandardCost * standardHours
        + OvertimeCost * overtimeHours
    )
    >= MinProfit
)


### Define the objective

model.setObjective(
    quicksum(Prices[p] * batches[p] for p in range(P))
    - quicksum(
        MachineCosts[m] * quicksum(TimeRequired[m][p] * batches[p] for p in range(P))
        for m in range(1, M)
    )
    - StandardCost * standardHours
    - OvertimeCost * overtimeHours,
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
