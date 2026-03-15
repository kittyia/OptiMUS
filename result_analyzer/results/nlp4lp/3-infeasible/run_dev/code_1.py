import os
import numpy as np
import json 
from gurobipy import Model, GRB, quicksum


model = Model("OptimizationProblem")

with open("data.json", "r") as f:
    data = json.load(f)


### Define the parameters

AdvertisingBudget = data["AdvertisingBudget"]

CostRadioAd = data["CostRadioAd"]

CostSocialMediaAd = data["CostSocialMediaAd"]

ExposureRadioAd = data["ExposureRadioAd"]

ExposureSocialMediaAd = data["ExposureSocialMediaAd"]

MinRadioAds = data["MinRadioAds"]

MaxRadioAds = data["MaxRadioAds"]

MinSocialMediaAds = data["MinSocialMediaAds"]


### Define the variables

RadioAds = model.addVar(vtype=GRB.INTEGER, name="RadioAds")

SocialMediaAds = model.addVar(vtype=GRB.INTEGER, name="SocialMediaAds")


### Define the constraints

model.addConstr(CostRadioAd * RadioAds + CostSocialMediaAd * SocialMediaAds <= AdvertisingBudget)

model.addConstr(RadioAds >= MinRadioAds)

model.addConstr(RadioAds <= MaxRadioAds)

model.addConstr(SocialMediaAds >= MinSocialMediaAds)


### Define the objective

model.setObjective(ExposureRadioAd * RadioAds + ExposureSocialMediaAd * SocialMediaAds, GRB.MAXIMIZE)


### Optimize the model

model.optimize()


### Output results safely

if model.status == GRB.OPTIMAL:
    print("Optimal Objective Value: ", model.ObjVal)
    with open("output_solution.txt", "w") as f:
        f.write(str(model.ObjVal))
else:
    print("Optimization ended with status:", model.status)
    with open("output_solution.txt", "w") as f:
        f.write(str(model.status))