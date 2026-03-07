
import os
import numpy as np
import json 
from gurobipy import Model, GRB, quicksum


model = Model("OptimizationProblem")

with open("data.json", "r") as f:
    data = json.load(f)




### Define the parameters

GoalYoung = data["GoalYoung"] # shape: [], definition: Total goal for clicks by young individuals

GoalOld = data["GoalOld"] # shape: [], definition: Total goal for clicks by old individuals

GoalUniqueYoung = data["GoalUniqueYoung"] # shape: [], definition: Total goal for unique clicks by young individuals

GoalUniqueOld = data["GoalUniqueOld"] # shape: [], definition: Total goal for unique clicks by old individuals

YoungClicks = data["YoungClicks"] # shape: ['NumAdTypes'], definition: Number of clicks by young individuals for each ad type

OldClicks = data["OldClicks"] # shape: ['NumAdTypes'], definition: Number of clicks by old individuals for each ad type

Costs = data["Costs"] # shape: ['NumAdTypes'], definition: Cost associated with each ad type

MaxClicks = data["MaxClicks"] # shape: ['NumAdTypes'], definition: Maximum number of clicks possible for each ad type

UniqueClicks = data["UniqueClicks"] # shape: ['NumAdTypes'], definition: Number of unique clicks for each ad type

NumAdTypes = data["NumAdTypes"] # shape: [], definition: Number of different ad types



### Define the variables

clicks = model.addVars(NumAdTypes, vtype=GRB.CONTINUOUS, name="clicks")



### Define the constraints

for a in range(NumAdTypes):
    model.addConstr(clicks[a] <= MaxClicks[a])
for a in range(NumAdTypes):
    model.addConstr(clicks[a] >= 0)
model.addConstr(
    sum(YoungClicks[a] * clicks[a] for a in range(NumAdTypes)) >= GoalYoung
)
model.addConstr(
    sum(OldClicks[a] * clicks[a] for a in range(NumAdTypes)) >= GoalOld
)
model.addConstr(
    sum(YoungClicks[a] * UniqueClicks[a] * clicks[a] for a in range(NumAdTypes))
    >= GoalUniqueYoung
)
model.addConstr(
    sum(OldClicks[a] * UniqueClicks[a] * clicks[a] for a in range(NumAdTypes))
    >= GoalUniqueOld
)


### Define the objective

model.setObjective(quicksum(Costs[a] * clicks[a] for a in range(NumAdTypes)), GRB.MINIMIZE)


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
