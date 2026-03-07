
import os
import numpy as np
import json 
from gurobipy import Model, GRB, quicksum


model = Model("OptimizationProblem")

with open("data.json", "r") as f:
    data = json.load(f)




### Define the parameters

PointsLimit = data["PointsLimit"] # shape: [], definition: Number of points available to distribute

MaxSeasonalPercentage = data["MaxSeasonalPercentage"] # shape: [], definition: Maximum percentage of volunteers that can be seasonal

MinFullTimeVolunteers = data["MinFullTimeVolunteers"] # shape: [], definition: Minimum number of full-time volunteers required

GiftsPerSeasonal = data["GiftsPerSeasonal"] # shape: [], definition: Number of gifts delivered by each seasonal volunteer

PointsPerSeasonal = data["PointsPerSeasonal"] # shape: [], definition: Points awarded to each seasonal volunteer

GiftsPerFullTime = data["GiftsPerFullTime"] # shape: [], definition: Number of gifts delivered by each full-time volunteer

PointsPerFullTime = data["PointsPerFullTime"] # shape: [], definition: Points awarded to each full-time volunteer



### Define the variables

SeasonalVolunteers = model.addVar(vtype=GRB.INTEGER, name="SeasonalVolunteers")

FullTimeVolunteers = model.addVar(vtype=GRB.INTEGER, name="FullTimeVolunteers")



### Define the constraints

model.addConstr(PointsPerSeasonal * SeasonalVolunteers + PointsPerFullTime * FullTimeVolunteers <= PointsLimit)
model.addConstr(7 * SeasonalVolunteers <= 3 * FullTimeVolunteers)
model.addConstr(FullTimeVolunteers >= MinFullTimeVolunteers)
model.addConstr(SeasonalVolunteers >= 0)


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
