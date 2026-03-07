
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

HighPressureTrips = model.addVar(vtype=GRB.INTEGER, name="HighPressureTrips")

LiquefiedTrips = model.addVar(vtype=GRB.INTEGER, name="LiquefiedTrips")



### Define the constraints

model.addConstr(50 * HighPressureTrips + 30 * LiquefiedTrips >= MinimumHydrogen)
model.addConstr(500 * HighPressureTrips + 200 * LiquefiedTrips <= Budget)
model.addConstr(HighPressureTrips <= LiquefiedTrips - 1)
model.addConstr(HighPressureTrips >= 0)
model.addConstr(LiquefiedTrips >= 0)


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
