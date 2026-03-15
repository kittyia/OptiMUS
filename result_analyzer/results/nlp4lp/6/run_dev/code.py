
import os
import numpy as np
import json 
from gurobipy import Model, GRB, quicksum


model = Model("OptimizationProblem")

with open("data.json", "r") as f:
    data = json.load(f)




### Define the parameters

CostZTube = data["CostZTube"] # shape: [], definition: Cost per advertisement on z-tube

ViewersZTube = data["ViewersZTube"] # shape: [], definition: Number of viewers attracted by each advertisement on z-tube

CostSoorchle = data["CostSoorchle"] # shape: [], definition: Cost per advertisement on soorchle

ViewersSoorchle = data["ViewersSoorchle"] # shape: [], definition: Number of viewers attracted by each advertisement on soorchle

CostWassa = data["CostWassa"] # shape: [], definition: Cost per advertisement on wassa

ViewersWassa = data["ViewersWassa"] # shape: [], definition: Number of viewers attracted by each advertisement on wassa

MaxAdsSoorchle = data["MaxAdsSoorchle"] # shape: [], definition: Maximum number of advertisements allowed on soorchle

MaxFractionWassaAds = data["MaxFractionWassaAds"] # shape: [], definition: Maximum fraction of total advertisements allowed on wassa

MinFractionZTubeAds = data["MinFractionZTubeAds"] # shape: [], definition: Minimum fraction of total advertisements required on z-tube

WeeklyAdvertisingBudget = data["WeeklyAdvertisingBudget"] # shape: [], definition: Weekly advertising budget



### Define the variables

AdsZTube = model.addVar(vtype=GRB.INTEGER, name="AdsZTube")

AdsSoorchle = model.addVar(vtype=GRB.INTEGER, name="AdsSoorchle")

AdsWassa = model.addVar(vtype=GRB.INTEGER, name="AdsWassa")



### Define the constraints

model.addConstr(CostZTube * AdsZTube + CostSoorchle * AdsSoorchle + CostWassa * AdsWassa <= WeeklyAdvertisingBudget)
model.addConstr(AdsSoorchle <= MaxAdsSoorchle)
model.addConstr(
    AdsWassa <= MaxFractionWassaAds * (AdsZTube + AdsSoorchle + AdsWassa)
)
model.addConstr(AdsZTube >= MinFractionZTubeAds * (AdsZTube + AdsSoorchle + AdsWassa))
model.addConstr(AdsZTube >= 0)  
model.addConstr(AdsSoorchle >= 0)  
model.addConstr(AdsWassa >= 0)


### Define the objective

model.setObjective(
    ViewersZTube * AdsZTube +
    ViewersSoorchle * AdsSoorchle +
    ViewersWassa * AdsWassa,
    GRB.MAXIMIZE
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
