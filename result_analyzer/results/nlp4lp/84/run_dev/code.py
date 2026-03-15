
import os
import numpy as np
import json 
from gurobipy import Model, GRB, quicksum


model = Model("OptimizationProblem")

with open("data.json", "r") as f:
    data = json.load(f)




### Define the parameters

NumReactions = data["NumReactions"] # shape: [], definition: Number of reaction types

NumResources = data["NumResources"] # shape: [], definition: Number of resource types

ResourceRequirement = data["ResourceRequirement"] # shape: ['NumReactions', 'NumResources'], definition: Units of resource j required for reaction i

ProductionPerReaction = data["ProductionPerReaction"] # shape: ['NumReactions'], definition: Units of rare compound produced by reaction i

ResourceAvailable = data["ResourceAvailable"] # shape: ['NumResources'], definition: Total units of resource j available



### Define the variables

ReactionCount = model.addVars(NumReactions, vtype=GRB.INTEGER, name="ReactionCount")



### Define the constraints

model.addConstr(5 * ReactionCount[0] + 7 * ReactionCount[1] <= 1000)
model.addConstr(6 * ReactionCount[0] + 3 * ReactionCount[1] <= 800)
for i in range(NumReactions):
    model.addConstr(ReactionCount[i] >= 0)


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
