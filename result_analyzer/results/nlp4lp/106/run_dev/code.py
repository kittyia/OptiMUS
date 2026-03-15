
import os
import numpy as np
import json 
from gurobipy import Model, GRB, quicksum


model = Model("OptimizationProblem")

with open("data.json", "r") as f:
    data = json.load(f)




### Define the parameters

NumFactories = data["NumFactories"] # shape: [], definition: Number of factories

NumProducts = data["NumProducts"] # shape: [], definition: Number of products

ProductionRate = data["ProductionRate"] # shape: ['NumFactories', 'NumProducts'], definition: Production rate of a product by a factory in units per hour

BaseGelRequirement = data["BaseGelRequirement"] # shape: ['NumFactories'], definition: Base gel required per hour by a factory

AvailableBaseGel = data["AvailableBaseGel"] # shape: [], definition: Total available units of base gel

MinimumDemand = data["MinimumDemand"] # shape: ['NumProducts'], definition: Minimum required units of each product



### Define the variables

HoursRun = model.addVars(NumFactories, vtype=GRB.CONTINUOUS, name="HoursRun")



### Define the constraints

model.addConstr(
    sum(BaseGelRequirement[i] * HoursRun[i] for i in range(NumFactories))
    <= AvailableBaseGel
)
model.addConstr(ProductionRate[0][0] * HoursRun[0] + ProductionRate[1][0] * HoursRun[1] >= MinimumDemand[0])
model.addConstr(15 * HoursRun[0] + 10 * HoursRun[1] >= 1000)
model.addConstr(HoursRun[0] >= 0)
model.addConstr(HoursRun[1] >= 0)


### Define the objective

model.setObjective(quicksum(HoursRun[f] for f in range(NumFactories)), GRB.MINIMIZE)


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
