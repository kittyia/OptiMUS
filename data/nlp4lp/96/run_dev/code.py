
import os
import numpy as np
import json 
from gurobipy import Model, GRB, quicksum


model = Model("OptimizationProblem")

with open("data.json", "r") as f:
    data = json.load(f)




### Define the parameters

NumFactories = data["NumFactories"] # shape: [], definition: Number of factories

NumProducts = data["NumProducts"] # shape: [], definition: Number of product types

ProductionRate = data["ProductionRate"] # shape: ['NumProducts', 'NumFactories'], definition: Production rate of product i in factory j per hour

ResourceRequirement = data["ResourceRequirement"] # shape: ['NumFactories'], definition: Resource requirement of factory j per hour

TotalResource = data["TotalResource"] # shape: [], definition: Total available units of the rare compound

MinProduction = data["MinProduction"] # shape: ['NumProducts'], definition: Minimum required production of product i



### Define the variables

Hours = model.addVars(NumFactories, vtype=GRB.CONTINUOUS, name="Hours")



### Define the constraints

model.addConstr(
    sum(ProductionRate[0][j] * Hours[j] for j in range(NumFactories)) >= 700
)
model.addConstr(
    sum(ProductionRate[1][j] * Hours[j] for j in range(NumFactories)) >= 600
)
model.addConstr(
    sum(ResourceRequirement[j] * Hours[j] for j in range(NumFactories)) <= TotalResource
)
for j in range(NumFactories):
    model.addConstr(Hours[j] >= 0)


### Define the objective

model.setObjective(quicksum(Hours[j] for j in range(NumFactories)), GRB.MINIMIZE)


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
