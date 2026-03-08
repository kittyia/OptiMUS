
import os
import numpy as np
import json 
from gurobipy import Model, GRB, quicksum


model = Model("OptimizationProblem")

with open("data.json", "r") as f:
    data = json.load(f)




### Define the parameters

AudiencePop = data["AudiencePop"] # shape: [], definition: Audience members brought in by one pop concert

AudienceRnB = data["AudienceRnB"] # shape: [], definition: Audience members brought in by one R&B concert

PracticeDaysPop = data["PracticeDaysPop"] # shape: [], definition: Number of practice days required for one pop concert

PracticeDaysRnB = data["PracticeDaysRnB"] # shape: [], definition: Number of practice days required for one R&B concert

MinAudience = data["MinAudience"] # shape: [], definition: Minimum required audience members

TotalPracticeDays = data["TotalPracticeDays"] # shape: [], definition: Total available practice days

MaxRnBProportion = data["MaxRnBProportion"] # shape: [], definition: Maximum proportion of concerts that can be R&B



### Define the variables

PopConcerts = model.addVar(vtype=GRB.INTEGER, name="PopConcerts")

RnBConcerts = model.addVar(vtype=GRB.INTEGER, name="RnBConcerts")



### Define the constraints

model.addConstr(AudiencePop * PopConcerts + AudienceRnB * RnBConcerts >= MinAudience)
model.addConstr(PracticeDaysPop * PopConcerts + PracticeDaysRnB * RnBConcerts <= TotalPracticeDays)
model.addConstr(RnBConcerts <= MaxRnBProportion * (PopConcerts + RnBConcerts))
model.addConstr(PopConcerts >= 0)
model.addConstr(RnBConcerts >= 0)


### Define the objective

model.setObjective(PopConcerts + RnBConcerts, GRB.MINIMIZE)


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
