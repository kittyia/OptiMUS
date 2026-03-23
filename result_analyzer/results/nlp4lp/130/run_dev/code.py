
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

minutesBeam1 = model.addVar(vtype=GRB.CONTINUOUS, name="minutesBeam1")

minutesBeam2 = model.addVar(vtype=GRB.CONTINUOUS, name="minutesBeam2")



### Define the constraints

model.addConstr(
    DoseRateBeam1BenignSkin * minutesBeam1 +
    DoseRateBeam2BenignSkin * minutesBeam2
    <= MaxDoseSkin
)
model.addConstr(DoseRateBeam1Tumor * minutesBeam1 + DoseRateBeam2Tumor * minutesBeam2 >= MinDoseTumor)
model.addConstr(minutesBeam1 >= 0)
model.addConstr(minutesBeam2 >= 0)


### Define the objective

model.setObjective(
    DoseRateBeam1BenignPancreas * minutesBeam1 +
    DoseRateBeam2BenignPancreas * minutesBeam2,
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
