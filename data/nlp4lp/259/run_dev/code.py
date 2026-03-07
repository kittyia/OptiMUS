
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

runnerTrips = model.addVar(vtype=GRB.INTEGER, name="runnerTrips")

canoeTrips = model.addVar(vtype=GRB.INTEGER, name="canoeTrips")



### Define the constraints

model.addConstr(RunnerTime * runnerTrips + CanoeTime * canoeTrips <= MaxTotalHours)
model.addConstr(canoeTrips <= MaxCanoePercentage * (runnerTrips + canoeTrips))
model.addConstr(runnerTrips >= MinRunners)
model.addConstr(canoeTrips >= 0)
model.addConstr(runnerTrips >= 0)
model.addConstr(canoeTrips >= 0)


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
