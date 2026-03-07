
import os
import numpy as np
import json 
from gurobipy import Model, GRB, quicksum


model = Model("OptimizationProblem")

with open("data.json", "r") as f:
    data = json.load(f)




### Define the parameters

CostFeedA = data["CostFeedA"] # shape: [], definition: Cost per kilogram of Feed A

CostFeedB = data["CostFeedB"] # shape: [], definition: Cost per kilogram of Feed B

ProteinFeedA = data["ProteinFeedA"] # shape: [], definition: Protein units per kilogram of Feed A

ProteinFeedB = data["ProteinFeedB"] # shape: [], definition: Protein units per kilogram of Feed B

FatFeedA = data["FatFeedA"] # shape: [], definition: Fat units per kilogram of Feed A

FatFeedB = data["FatFeedB"] # shape: [], definition: Fat units per kilogram of Feed B

MinProtein = data["MinProtein"] # shape: [], definition: Minimum required units of protein in the mixture

MinFat = data["MinFat"] # shape: [], definition: Minimum required units of fat in the mixture



### Define the variables

FeedAkg = model.addVar(vtype=GRB.CONTINUOUS, name="FeedAkg")

FeedBkg = model.addVar(vtype=GRB.CONTINUOUS, name="FeedBkg")



### Define the constraints

model.addConstr(ProteinFeedA * FeedAkg + ProteinFeedB * FeedBkg >= MinProtein)
model.addConstr(FatFeedA * FeedAkg + FatFeedB * FeedBkg >= MinFat)
model.addConstr(FeedAkg >= 0)
model.addConstr(FeedBkg >= 0)


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
