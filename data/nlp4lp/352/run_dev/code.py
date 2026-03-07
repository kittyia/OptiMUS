
import os
import numpy as np
import json 
from gurobipy import Model, GRB, quicksum


model = Model("OptimizationProblem")

with open("data.json", "r") as f:
    data = json.load(f)




### Define the parameters

N = data["N"] # shape: [], definition: Number of interventions

IsolateCentral = data["IsolateCentral"] # shape: ['N'], definition: Processing time for isolating at the central system for each intervention

ScanCentral = data["ScanCentral"] # shape: ['N'], definition: Processing time for scanning at the central system for each intervention

IsolateDistributed = data["IsolateDistributed"] # shape: ['N'], definition: Processing time for isolating at the distributed system for each intervention

ScanDistributed = data["ScanDistributed"] # shape: ['N'], definition: Processing time for scanning at the distributed system for each intervention

CentralCost = data["CentralCost"] # shape: [], definition: Cost for central system intervention

DistributedCost = data["DistributedCost"] # shape: [], definition: Cost for distributed system intervention

CentralMaxHours = data["CentralMaxHours"] # shape: [], definition: Maximum hours of operation for the central system

DistributedMaxHours = data["DistributedMaxHours"] # shape: [], definition: Maximum hours of operation for the distributed system



### Define the variables

isolateCentral = model.addVars(N, vtype=GRB.BINARY, name="isolateCentral")

isolateDistributed = model.addVars(N, vtype=GRB.BINARY, name="isolateDistributed")

scanCentral = model.addVars(N, vtype=GRB.BINARY, name="scanCentral")

scanDistributed = model.addVars(N, vtype=GRB.BINARY, name="scanDistributed")



### Define the constraints

for i in range(N):
    model.addConstr(
        isolateCentral[i] 
        + isolateDistributed[i] 
        + scanCentral[i] 
        + scanDistributed[i] 
        == 1
    )
model.addConstr(
    sum(IsolateCentral[i] * isolateCentral[i] + 
        ScanCentral[i] * scanCentral[i] 
        for i in range(N)) 
    <= CentralMaxHours
)
model.addConstr(
    sum(
        isolateDistributed[i] * IsolateDistributed[i] +
        scanDistributed[i] * ScanDistributed[i]
        for i in range(N)
    ) <= DistributedMaxHours
)
for i in range(N):
    model.addConstr(isolateCentral[i] >= 0)
    model.addConstr(isolateCentral[i] <= 1)
    
    model.addConstr(isolateDistributed[i] >= 0)
    model.addConstr(isolateDistributed[i] <= 1)
    
    model.addConstr(scanCentral[i] >= 0)
    model.addConstr(scanCentral[i] <= 1)
    
    model.addConstr(scanDistributed[i] >= 0)
    model.addConstr(scanDistributed[i] <= 1)


### Define the objective

model.setObjective(
    CentralCost * quicksum(
        IsolateCentral[i] * isolateCentral[i] + 
        ScanCentral[i] * scanCentral[i]
        for i in range(N)
    )
    +
    DistributedCost * quicksum(
        IsolateDistributed[i] * isolateDistributed[i] + 
        ScanDistributed[i] * scanDistributed[i]
        for i in range(N)
    ),
    GRB.MINIMIZE
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
