
import os
import numpy as np
import json 
from gurobipy import Model, GRB, quicksum


model = Model("OptimizationProblem")

with open("data.json", "r") as f:
    data = json.load(f)




### Define the parameters

TotalAcres = data["TotalAcres"] # shape: [], definition: Total number of acres available for processing hay

NumMachines = data["NumMachines"] # shape: [], definition: Number of different machine types available for processing hay

FuelAvailable = data["FuelAvailable"] # shape: [], definition: Total amount of fuel available

MethaneLimit = data["MethaneLimit"] # shape: [], definition: Maximum allowable amount of methane gas production

HayProcessedPerAcre = data["HayProcessedPerAcre"] # shape: ['NumMachines'], definition: Amount of hay processed per acre by each machine type

MethaneProducedPerAcre = data["MethaneProducedPerAcre"] # shape: ['NumMachines'], definition: Amount of methane gas produced per acre by each machine type

FuelRequiredPerAcre = data["FuelRequiredPerAcre"] # shape: ['NumMachines'], definition: Amount of fuel required per acre by each machine type



### Define the variables

AcresUsed = model.addVars(NumMachines, vtype=GRB.CONTINUOUS, name="AcresUsed")



### Define the constraints

model.addConstr(
    sum(AcresUsed[m] for m in range(NumMachines)) <= TotalAcres
)
model.addConstr(
    sum(FuelRequiredPerAcre[m] * AcresUsed[m] for m in range(NumMachines)) 
    <= FuelAvailable
)
for i in range(NumMachines):
    model.addConstr(AcresUsed[i] >= 0)


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
