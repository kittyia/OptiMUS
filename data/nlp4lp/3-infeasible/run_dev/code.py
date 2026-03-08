
import os
import numpy as np
import json 
from gurobipy import Model, GRB, quicksum


model = Model("OptimizationProblem")

with open("data.json", "r") as f:
    data = json.load(f)




### Define the parameters

AdvertisingBudget = data["AdvertisingBudget"] # shape: [], definition: The total advertising budget available

CostRadioAd = data["CostRadioAd"] # shape: [], definition: Cost of one radio advertisement

CostSocialMediaAd = data["CostSocialMediaAd"] # shape: [], definition: Cost of one social media advertisement

ExposureRadioAd = data["ExposureRadioAd"] # shape: [], definition: Expected exposure (viewers) for each radio advertisement

ExposureSocialMediaAd = data["ExposureSocialMediaAd"] # shape: [], definition: Expected exposure (viewers) for each social media advertisement

MinRadioAds = data["MinRadioAds"] # shape: [], definition: Minimum number of radio advertisements to be ordered

MaxRadioAds = data["MaxRadioAds"] # shape: [], definition: Maximum number of radio advertisements to be ordered

MinSocialMediaAds = data["MinSocialMediaAds"] # shape: [], definition: Minimum number of social media advertisements to be contracted



### Define the variables

RadioAds = model.addVar(vtype=GRB.INTEGER, name="RadioAds")

SocialMediaAds = model.addVar(vtype=GRB.INTEGER, name="SocialMediaAds")



### Define the constraints

model.addConstr(CostRadioAd * RadioAds + CostSocialMediaAd * SocialMediaAds <= AdvertisingBudget)
model.addConstr(RadioAds >= MinRadioAds)
model.addConstr(RadioAds <= MaxRadioAds)
model.addConstr(SocialMediaAds >= MinSocialMediaAds)
# RadioAds is defined as an integer variable (vtype=GRB.INTEGER), 
# so no additional constraint is required to enforce integrality.
# SocialMediaAds is defined as an integer variable (vtype=GRB.INTEGER), 
# so no additional constraint is required to enforce integrality.


### Define the objective

model.setObjective(ExposureRadioAd * RadioAds + ExposureSocialMediaAd * SocialMediaAds, GRB.MAXIMIZE)


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
