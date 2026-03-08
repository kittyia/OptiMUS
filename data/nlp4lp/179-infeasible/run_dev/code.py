
import os
import numpy as np
import json 
from gurobipy import Model, GRB, quicksum


model = Model("OptimizationProblem")

with open("data.json", "r") as f:
    data = json.load(f)




### Define the parameters

TransportCapacity = data["TransportCapacity"] # shape: ['NumTransportMethods'], definition: Transport capacity per trip for each transportation method

TransportCost = data["TransportCost"] # shape: ['NumTransportMethods'], definition: Transport cost per trip for each transportation method

MinimumHydrogen = data["MinimumHydrogen"] # shape: [], definition: Minimum total hydrogen to transport

Budget = data["Budget"] # shape: [], definition: Available budget for transportation

NumTransportMethods = data["NumTransportMethods"] # shape: [], definition: Number of transportation methods



### Define the variables

NumTrips = model.addVars(NumTransportMethods, vtype=GRB.INTEGER, name="NumTrips")



### Define the constraints

model.addConstr(
    sum(TransportCapacity[m] * NumTrips[m] for m in range(NumTransportMethods)) 
    >= MinimumHydrogen
)
model.addConstr(
    sum(TransportCost[m] * NumTrips[m] for m in range(NumTransportMethods)) <= Budget
)
model.addConstr(NumTrips[0] + 1 <= NumTrips[1])
for m in range(NumTransportMethods):
    model.addConstr(NumTrips[m] >= 0)


### Define the objective

model.setObjective(quicksum(NumTrips[i] for i in range(NumTransportMethods)), GRB.MINIMIZE)


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
