
import os
import numpy as np
import json 
from gurobipy import Model, GRB, quicksum


model = Model("OptimizationProblem")

with open("data.json", "r") as f:
    data = json.load(f)




### Define the parameters

NumProducts = data["NumProducts"] # shape: [], definition: Number of different sports equipment produced

MaterialRequirement = data["MaterialRequirement"] # shape: ['NumProducts'], definition: Amount of materials required to produce one unit of each sports equipment

TimeRequirement = data["TimeRequirement"] # shape: ['NumProducts'], definition: Amount of labor hours required to produce one unit of each sports equipment

TotalMaterialsAvailable = data["TotalMaterialsAvailable"] # shape: [], definition: Total units of materials available for production

TotalLaborHoursAvailable = data["TotalLaborHoursAvailable"] # shape: [], definition: Total labor hours available for production

MinBasketballToFootballRatio = data["MinBasketballToFootballRatio"] # shape: [], definition: Minimum ratio of basketballs to footballs production

MinimumFootballs = data["MinimumFootballs"] # shape: [], definition: Minimum number of footballs to produce



### Define the variables

Basketballs = model.addVar(vtype=GRB.INTEGER, name="Basketballs")

Footballs = model.addVar(vtype=GRB.INTEGER, name="Footballs")



### Define the constraints

model.addConstr(5 * Basketballs + 3 * Footballs <= TotalMaterialsAvailable)
model.addConstr(Basketballs + 2 * Footballs <= TotalLaborHoursAvailable)
model.addConstr(Basketballs >= MinBasketballToFootballRatio * Footballs)
model.addConstr(Footballs >= MinimumFootballs)


### Define the objective

del.setObjective(Basketballs + Footballs, GRB.MAXIMIZE


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
