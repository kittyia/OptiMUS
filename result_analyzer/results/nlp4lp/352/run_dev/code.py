
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

IsolateCentralChoice = model.addVars(N, vtype=GRB.BINARY, name="IsolateCentralChoice")

ScanCentralChoice = model.addVars(N, vtype=GRB.BINARY, name="ScanCentralChoice")

IsolateDistributedChoice = model.addVars(N, vtype=GRB.BINARY, name="IsolateDistributedChoice")

ScanDistributedChoice = model.addVars(N, vtype=GRB.BINARY, name="ScanDistributedChoice")



### Define the constraints

for i in range(N):
    model.addConstr(IsolateCentralChoice[i] >= 0)
    model.addConstr(IsolateCentralChoice[i] <= 1)
    
    model.addConstr(ScanCentralChoice[i] >= 0)
    model.addConstr(ScanCentralChoice[i] <= 1)
    
    model.addConstr(IsolateDistributedChoice[i] >= 0)
    model.addConstr(IsolateDistributedChoice[i] <= 1)
    
    model.addConstr(ScanDistributedChoice[i] >= 0)
    model.addConstr(ScanDistributedChoice[i] <= 1)
for i in range(N):
    model.addConstr(
        IsolateCentralChoice[i] +
        ScanCentralChoice[i] +
        IsolateDistributedChoice[i] +
        ScanDistributedChoice[i] == 1
    )
model.addConstr(
    sum(
        IsolateCentral[i] * IsolateCentralChoice[i] +
        ScanCentral[i] * ScanCentralChoice[i]
        for i in range(N)
    ) <= CentralMaxHours
)
model.addConstr(
    sum(
        IsolateDistributed[i] * IsolateDistributedChoice[i] +
        ScanDistributed[i] * ScanDistributedChoice[i]
        for i in range(N)
    ) <= DistributedMaxHours
)


### Define the objective

model.setObjective(
    CentralCost * quicksum(
        IsolateCentral[i] * IsolateCentralChoice[i] +
        ScanCentral[i] * ScanCentralChoice[i]
        for i in range(N)
    )
    +
    DistributedCost * quicksum(
        IsolateDistributed[i] * IsolateDistributedChoice[i] +
        ScanDistributed[i] * ScanDistributedChoice[i]
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
