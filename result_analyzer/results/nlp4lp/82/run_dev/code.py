
import os
import numpy as np
import json 
from gurobipy import Model, GRB, quicksum


model = Model("OptimizationProblem")

with open("data.json", "r") as f:
    data = json.load(f)




### Define the parameters

NumFactoryTypes = data["NumFactoryTypes"] # shape: [], definition: Number of factory types

ProductionRate = data["ProductionRate"] # shape: ['NumFactoryTypes'], definition: Production rate of each factory type (toys per day)

OperatorRequirement = data["OperatorRequirement"] # shape: ['NumFactoryTypes'], definition: Number of operators required for each factory type

TotalProductionRequirement = data["TotalProductionRequirement"] # shape: [], definition: Minimum number of toys required per day

TotalAvailableOperators = data["TotalAvailableOperators"] # shape: [], definition: Total number of available operators



### Define the variables

NumFactories = model.addVars(NumFactoryTypes, vtype=GRB.INTEGER, name="NumFactories")



### Define the constraints

model.addConstr(
    sum(ProductionRate[i] * NumFactories[i] for i in range(NumFactoryTypes)) 
    >= TotalProductionRequirement
)
model.addConstr(
    quicksum(OperatorRequirement[i] * NumFactories[i] for i in range(NumFactoryTypes))
    <= TotalAvailableOperators
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
