
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

numPiTV = model.addVar(vtype=GRB.INTEGER, name="numPiTV")

numBetaVideo = model.addVar(vtype=GRB.INTEGER, name="numBetaVideo")

numGammaLive = model.addVar(vtype=GRB.INTEGER, name="numGammaLive")



### Define the constraints

model.addConstr(CostPiTV * numPiTV + CostBetaVideo * numBetaVideo + CostGammaLive * numGammaLive <= TotalBudget)
model.addConstr(numBetaVideo <= MaxCommercialsBetaVideo)
model.addConstr(
    numGammaLive <= MaxGammaProportion * (numPiTV + numBetaVideo + numGammaLive)
)
model.addConstr(
    numPiTV >= MinPiTVProportion * (numPiTV + numBetaVideo + numGammaLive)
)
model.addConstr(numPiTV >= 0)
model.addConstr(numBetaVideo >= 0)
model.addConstr(numGammaLive >= 0)


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
