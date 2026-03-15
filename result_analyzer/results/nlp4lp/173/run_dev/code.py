
import os
import numpy as np
import json 
from gurobipy import Model, GRB, quicksum


model = Model("OptimizationProblem")

with open("data.json", "r") as f:
    data = json.load(f)




### Define the parameters

VisitorsPerBalloon = data["VisitorsPerBalloon"] # shape: [], definition: Number of visitors that can be carried by one hot-air balloon

VisitorsPerGondola = data["VisitorsPerGondola"] # shape: [], definition: Number of visitors that can be carried by one gondola lift

PollutionPerBalloon = data["PollutionPerBalloon"] # shape: [], definition: Units of pollution produced by one hot-air balloon ride

PollutionPerGondola = data["PollutionPerGondola"] # shape: [], definition: Units of pollution produced by one gondola lift ride

MaxBalloonRides = data["MaxBalloonRides"] # shape: [], definition: Maximum number of hot-air balloon rides allowed

MinVisitors = data["MinVisitors"] # shape: [], definition: Minimum number of visitors that need to be transported



### Define the variables

BalloonRides = model.addVar(vtype=GRB.INTEGER, name="BalloonRides")

GondolaRides = model.addVar(vtype=GRB.INTEGER, name="GondolaRides")



### Define the constraints

model.addConstr(BalloonRides <= MaxBalloonRides)
model.addConstr(VisitorsPerBalloon * BalloonRides + VisitorsPerGondola * GondolaRides >= MinVisitors)
model.addConstr(BalloonRides >= 0)
model.addConstr(GondolaRides >= 0)


### Define the objective

model.setObjective(
    PollutionPerBalloon * BalloonRides +
    PollutionPerGondola * GondolaRides,
    GRB.MINIMIZE
)


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
