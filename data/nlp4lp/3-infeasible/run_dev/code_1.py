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

model.addConstr(CostRadioAd * RadioAds + CostSocialMediaAd * SocialMediaAds <= AdvertisingBudget, name="Budget")
model.addConstr(RadioAds >= MinRadioAds, name="MinRadioAds")
model.addConstr(RadioAds <= MaxRadioAds, name="MaxRadioAds")
model.addConstr(SocialMediaAds >= MinSocialMediaAds, name="MinSocialMediaAds")

### Define the objective (maximize total exposure)

model.setObjective(
    ExposureRadioAd * RadioAds + ExposureSocialMediaAd * SocialMediaAds,
    GRB.MAXIMIZE
)

### Optimize the model

model.optimize()

### Output optimal objective value

if model.status == GRB.OPTIMAL:
    print("Optimal Objective Value: ", model.ObjVal)
    with open("output_solution.txt", "w") as f:
        f.write(str(model.ObjVal))
else:
    with open("output_solution.txt", "w") as f:
        f.write(str(model.status))