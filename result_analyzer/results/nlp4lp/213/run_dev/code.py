
import os
import numpy as np
import json 
from gurobipy import Model, GRB, quicksum


model = Model("OptimizationProblem")

with open("data.json", "r") as f:
    data = json.load(f)




### Define the parameters

CostPiTV = data["CostPiTV"] # shape: [], definition: Cost per commercial on Pi TV

CostBetaVideo = data["CostBetaVideo"] # shape: [], definition: Cost per commercial on Beta Video

CostGammaLive = data["CostGammaLive"] # shape: [], definition: Cost per commercial on Gamma Live

AudiencePiTV = data["AudiencePiTV"] # shape: [], definition: Audience per commercial on Pi TV

AudienceBetaVideo = data["AudienceBetaVideo"] # shape: [], definition: Audience per commercial on Beta Video

AudienceGammaLive = data["AudienceGammaLive"] # shape: [], definition: Audience per commercial on Gamma Live

MaxCommercialsBetaVideo = data["MaxCommercialsBetaVideo"] # shape: [], definition: Maximum number of commercials on Beta Video

TotalBudget = data["TotalBudget"] # shape: [], definition: Total weekly budget

MaxGammaProportion = data["MaxGammaProportion"] # shape: [], definition: Maximum proportion of all commercials on Gamma Live

MinPiTVProportion = data["MinPiTVProportion"] # shape: [], definition: Minimum proportion of all commercials on Pi TV



### Define the variables

NumPiTV = model.addVar(vtype=GRB.INTEGER, name="NumPiTV")

NumBetaVideo = model.addVar(vtype=GRB.INTEGER, name="NumBetaVideo")

NumGammaLive = model.addVar(vtype=GRB.INTEGER, name="NumGammaLive")



### Define the constraints

model.addConstr(
    CostPiTV * NumPiTV 
    + CostBetaVideo * NumBetaVideo 
    + CostGammaLive * NumGammaLive 
    <= TotalBudget
)
model.addConstr(NumBetaVideo <= MaxCommercialsBetaVideo)
model.addConstr(3 * NumGammaLive <= NumPiTV + NumBetaVideo + NumGammaLive)
model.addConstr(
    NumPiTV >= MinPiTVProportion * (NumPiTV + NumBetaVideo + NumGammaLive)
)
model.addConstr(NumPiTV >= 0)
model.addConstr(NumBetaVideo >= 0)
model.addConstr(NumGammaLive >= 0)


### Define the objective

model.setObjective(
    AudiencePiTV * NumPiTV +
    AudienceBetaVideo * NumBetaVideo +
    AudienceGammaLive * NumGammaLive,
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
