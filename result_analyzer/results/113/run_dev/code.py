
import os
import numpy as np
import json 
from gurobipy import Model, GRB, quicksum


model = Model("OptimizationProblem")

with open("data.json", "r") as f:
    data = json.load(f)




### Define the parameters

TotalMorphine = data["TotalMorphine"] # shape: [], definition: Total amount of morphine available

MorphinePerPainkiller = data["MorphinePerPainkiller"] # shape: [], definition: Amount of morphine required for one painkiller pill

MorphinePerSleepingPill = data["MorphinePerSleepingPill"] # shape: [], definition: Amount of morphine required for one sleeping pill

DigestiveMedicinePerPainkiller = data["DigestiveMedicinePerPainkiller"] # shape: [], definition: Amount of digestive medicine required for one painkiller pill

DigestiveMedicinePerSleepingPill = data["DigestiveMedicinePerSleepingPill"] # shape: [], definition: Amount of digestive medicine required for one sleeping pill

MinPainkillerPills = data["MinPainkillerPills"] # shape: [], definition: Minimum number of painkiller pills to be produced

MinSleepingPillsProportion = data["MinSleepingPillsProportion"] # shape: [], definition: Minimum proportion of pills that should be sleeping pills



### Define the variables

PainkillerPills = model.addVar(vtype=GRB.INTEGER, name="PainkillerPills")

SleepingPills = model.addVar(vtype=GRB.INTEGER, name="SleepingPills")



### Define the constraints

model.addConstr(
    MorphinePerPainkiller * PainkillerPills + 
    MorphinePerSleepingPill * SleepingPills 
    <= TotalMorphine
)
model.addConstr(PainkillerPills >= MinPainkillerPills)
model.addConstr(
    SleepingPills >= MinSleepingPillsProportion * (PainkillerPills + SleepingPills)
)


### Define the objective

model.setObjective(
    DigestiveMedicinePerPainkiller * PainkillerPills +
    DigestiveMedicinePerSleepingPill * SleepingPills,
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
