
import os
import numpy as np
import json 
from gurobipy import Model, GRB, quicksum


model = Model("OptimizationProblem")

with open("data.json", "r") as f:
    data = json.load(f)




### Define the parameters

NumFactoryTypes = data["NumFactoryTypes"] # shape: [], definition: Number of factory types

ProductionRate = data["ProductionRate"] # shape: ['NumFactoryTypes'], definition: Production rate of each factory type in phones per day

ManagerRequirement = data["ManagerRequirement"] # shape: ['NumFactoryTypes'], definition: Number of managers required for each factory type

AvailableManagers = data["AvailableManagers"] # shape: [], definition: Total number of managers available

RequiredPhones = data["RequiredPhones"] # shape: [], definition: Minimum number of phones required per day



### Define the variables

NumFactories = model.addVars(NumFactoryTypes, vtype=GRB.INTEGER, name="NumFactories")



### Define the constraints

model.addConstr(
    sum(ManagerRequirement[i] * NumFactories[i] for i in range(NumFactoryTypes))
    <= AvailableManagers
)
model.addConstr(
    sum(ProductionRate[i] * NumFactories[i] for i in range(NumFactoryTypes)) 
    >= RequiredPhones
)
for i in range(NumFactoryTypes):
    model.addConstr(NumFactories[i] >= 0)


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
