
import os
import numpy as np
import json 
from gurobipy import Model, GRB, quicksum


model = Model("OptimizationProblem")

with open("data.json", "r") as f:
    data = json.load(f)




### Define the parameters

NumFactories = data["NumFactories"] # shape: [], definition: The number of different factories available for production

NumColors = data["NumColors"] # shape: [], definition: The number of different colored teddy bears produced

FactoryRunningCost = data["FactoryRunningCost"] # shape: ['NumFactories'], definition: The cost to run each factory for one hour

ProductionRate = data["ProductionRate"] # shape: ['NumFactories', 'NumColors'], definition: The number of teddy bears of each color produced per hour by each factory

Demand = data["Demand"] # shape: ['NumColors'], definition: The minimum number of teddy bears of each color required per day



### Define the variables

FactoryHours = model.addVars(NumFactories, vtype=GRB.CONTINUOUS, name="FactoryHours")



### Define the constraints

model.addConstr(
    sum(ProductionRate[f][0] * FactoryHours[f] for f in range(NumFactories)) >= 20
)
model.addConstr(
    sum(ProductionRate[f][1] * FactoryHours[f] for f in range(NumFactories)) >= 5
)
model.addConstr(
    sum(ProductionRate[f][2] * FactoryHours[f] for f in range(NumFactories)) >= 15
)
for i in range(NumFactories):
    model.addConstr(FactoryHours[i] >= 0)


### Define the objective

model.setObjective(quicksum(FactoryRunningCost[i] * FactoryHours[i] for i in range(NumFactories)), GRB.MINIMIZE)


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
