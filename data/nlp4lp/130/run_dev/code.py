
import os
import numpy as np
import json 
from gurobipy import Model, GRB, quicksum


model = Model("OptimizationProblem")

with open("data.json", "r") as f:
    data = json.load(f)




### Define the parameters

DoseRateBeam1BenignPancreas = data["DoseRateBeam1BenignPancreas"] # shape: [], definition: Dose delivered per minute by Beam 1 to the benign area of the pancreas

DoseRateBeam1BenignSkin = data["DoseRateBeam1BenignSkin"] # shape: [], definition: Dose delivered per minute by Beam 1 to the benign area of the skin

DoseRateBeam1Tumor = data["DoseRateBeam1Tumor"] # shape: [], definition: Dose delivered per minute by Beam 1 to the tumor

DoseRateBeam2BenignPancreas = data["DoseRateBeam2BenignPancreas"] # shape: [], definition: Dose delivered per minute by Beam 2 to the benign area of the pancreas

DoseRateBeam2BenignSkin = data["DoseRateBeam2BenignSkin"] # shape: [], definition: Dose delivered per minute by Beam 2 to the benign area of the skin

DoseRateBeam2Tumor = data["DoseRateBeam2Tumor"] # shape: [], definition: Dose delivered per minute by Beam 2 to the tumor

MaxDoseSkin = data["MaxDoseSkin"] # shape: [], definition: Maximum allowable dose to the skin

MinDoseTumor = data["MinDoseTumor"] # shape: [], definition: Minimum required dose to the tumor



### Define the variables

Beam1Minutes = model.addVar(vtype=GRB.CONTINUOUS, name="Beam1Minutes")

Beam2Minutes = model.addVar(vtype=GRB.CONTINUOUS, name="Beam2Minutes")



### Define the constraints

model.addConstr(DoseRateBeam1BenignSkin * Beam1Minutes + DoseRateBeam2BenignSkin * Beam2Minutes <= MaxDoseSkin)
model.addConstr(DoseRateBeam1Tumor * Beam1Minutes + DoseRateBeam2Tumor * Beam2Minutes >= MinDoseTumor)
model.addConstr(Beam1Minutes >= 0)
model.addConstr(Beam2Minutes >= 0)


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
