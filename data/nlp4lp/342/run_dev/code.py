
import os
import numpy as np
import json 
from gurobipy import Model, GRB, quicksum


model = Model("OptimizationProblem")

with open("data.json", "r") as f:
    data = json.load(f)




### Define the parameters

A = data["A"] # shape: [], definition: Number of advertisement types

Budget = data["Budget"] # shape: [], definition: Total budget for purchasing clicks

Costs = data["Costs"] # shape: ['A'], definition: Cost of purchasing a click from advertisement type a

MaxClicks = data["MaxClicks"] # shape: ['A'], definition: Number of maximum clicks that can be purchased from advertisement type a

YoungClicks = data["YoungClicks"] # shape: ['A'], definition: Number of young audience clicks from advertisement type a

OldClicks = data["OldClicks"] # shape: ['A'], definition: Number of old audience clicks from advertisement type a

UniqueClicks = data["UniqueClicks"] # shape: ['A'], definition: Number of unique clicks from advertisement type a

GoalYoung = data["GoalYoung"] # shape: [], definition: Goal for number of clicks from young audience

GoalOld = data["GoalOld"] # shape: [], definition: Goal for number of clicks from old audience

GoalUniqueYoung = data["GoalUniqueYoung"] # shape: [], definition: Goal for number of unique clicks from young audience

GoalUniqueOld = data["GoalUniqueOld"] # shape: [], definition: Goal for number of unique clicks from old audience



### Define the variables

clicks = model.addVars(A, vtype=GRB.CONTINUOUS, name="clicks")



### Define the constraints

for a in range(A):
    model.addConstr(clicks[a] >= 0)
for a in range(A):
    model.addConstr(clicks[a] <= MaxClicks[a])
model.addConstr(
    sum(Costs[a] * clicks[a] for a in range(A)) <= Budget
)
model.addConstr(
    sum(YoungClicks[a] * clicks[a] for a in range(A)) >= GoalYoung
)
model.addConstr(
    sum(OldClicks[a] * clicks[a] for a in range(A)) >= GoalOld
)
model.addConstr(
    sum(clicks[a] * YoungClicks[a] * UniqueClicks[a] for a in range(A)) 
    >= GoalUniqueYoung
)
model.addConstr(
    sum(clicks[a] * UniqueClicks[a] * OldClicks[a] for a in range(A)) 
    >= GoalUniqueOld
)


### Define the objective

model.setObjective(quicksum(UniqueClicks[a] * clicks[a] for a in range(A)), GRB.MAXIMIZE)


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
