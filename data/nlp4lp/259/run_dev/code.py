
import os
import numpy as np
import json 
from gurobipy import Model, GRB, quicksum


model = Model("OptimizationProblem")

with open("data.json", "r") as f:
    data = json.load(f)




### Define the parameters

RunnerCapacity = data["RunnerCapacity"] # shape: [], definition: Number of bags a runner can carry each trip

RunnerTime = data["RunnerTime"] # shape: [], definition: Time a runner takes per trip (in hours)

CanoeCapacity = data["CanoeCapacity"] # shape: [], definition: Number of bags a canoeer can carry each trip

CanoeTime = data["CanoeTime"] # shape: [], definition: Time a canoeer takes per trip (in hours)

MaxCanoePercentage = data["MaxCanoePercentage"] # shape: [], definition: Maximum fraction of total deliveries that can be made by canoe

MaxTotalHours = data["MaxTotalHours"] # shape: [], definition: Maximum total hours the village can spare for deliveries

MinRunners = data["MinRunners"] # shape: [], definition: Minimum number of runners that must be used



### Define the variables

RunnerTrips = model.addVar(vtype=GRB.INTEGER, name="RunnerTrips")

CanoeTrips = model.addVar(vtype=GRB.INTEGER, name="CanoeTrips")



### Define the constraints

model.addConstr(RunnerTime * RunnerTrips + CanoeTime * CanoeTrips <= MaxTotalHours)
model.addConstr(67 * CanoeTrips <= 33 * RunnerTrips)
model.addConstr(RunnerTrips >= MinRunners)
model.addConstr(CanoeTrips >= 0)
model.addConstr(RunnerTrips >= 0)
model.addConstr(CanoeTrips >= 0)


### Define the objective

model.setObjective(RunnerCapacity * RunnerTrips + CanoeCapacity * CanoeTrips, GRB.MAXIMIZE)


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
