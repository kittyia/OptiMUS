
import os
import numpy as np
import json 
from gurobipy import Model, GRB, quicksum


model = Model("OptimizationProblem")

with open("data.json", "r") as f:
    data = json.load(f)




### Define the parameters

N = data["N"] # shape: [], definition: Number of computer systems

IsWorkstation = data["IsWorkstation"] # shape: ['N'], definition: Whether system i is a workstation (true) or general-purpose (false)

Price = data["Price"] # shape: ['N'], definition: Price of system i in dollars

DiskDrives = data["DiskDrives"] # shape: ['N'], definition: Average number of disk drives per unit of system i

MemoryBoards = data["MemoryBoards"] # shape: ['N'], definition: Number of 256K memory boards per unit of system i

MaxCpu = data["MaxCpu"] # shape: [], definition: Maximum number of CPUs available

MinDisk = data["MinDisk"] # shape: [], definition: Minimum available disk drive supply

MaxDisk = data["MaxDisk"] # shape: [], definition: Maximum available disk drive supply

MinMemory = data["MinMemory"] # shape: [], definition: Minimum available memory board supply

MaxMemory = data["MaxMemory"] # shape: [], definition: Maximum available memory board supply

Demand = data["Demand"] # shape: ['N'], definition: Maximum demand for system i

DemandGP = data["DemandGP"] # shape: [], definition: Maximum total demand for all general-purpose systems

DemandWS = data["DemandWS"] # shape: [], definition: Maximum total demand for all workstation systems

Preorder = data["Preorder"] # shape: ['N'], definition: Number of pre-orders for system i that must be fulfilled

AltMemory = data["AltMemory"] # shape: [], definition: Number of alternative memory boards available

AltCompatible = data["AltCompatible"] # shape: ['N'], definition: Whether alternative memory board is compatible with system i



### Define the variables

x = model.addVars(N, vtype=GRB.CONTINUOUS, name="x")

r = model.addVars(N, vtype=GRB.CONTINUOUS, name="r")

a = model.addVars(N, vtype=GRB.CONTINUOUS, name="a")



### Define the constraints

for i in range(N):
    model.addConstr(x[i] >= Preorder[i])
for i in range(N):
    model.addConstr(x[i] <= Demand[i])
model.addConstr(sum(x[i] for i in range(N)) <= MaxCpu)
model.addConstr(
    sum(DiskDrives[i] * x[i] for i in range(N)) <= MaxDisk
)
for i in range(N):
    model.addConstr(r[i] + a[i] == MemoryBoards[i] * x[i])
model.addConstr(sum(r[i] for i in range(N)) <= MaxMemory)
model.addConstr(sum(a[i] for i in range(N)) <= AltMemory)
for i in range(N):
    model.addConstr(a[i] <= AltCompatible[i] * MemoryBoards[i] * x[i])
model.addConstr(
    sum(x[i] for i in range(N) if IsWorkstation[i] == "false") <= DemandGP
)
model.addConstr(
    sum(x[i] for i in range(N) if IsWorkstation[i] == "true") <= DemandWS
)
for i in range(N):
    model.addConstr(x[i] >= 0)
    model.addConstr(r[i] >= 0)
    model.addConstr(a[i] >= 0)


### Define the objective

model.setObjective(quicksum(Price[i] * x[i] for i in range(N)), GRB.MAXIMIZE)


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
