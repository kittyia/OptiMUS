import os
import numpy as np
import json
from gurobipy import Model, GRB, quicksum


model = Model("OptimizationProblem")

with open("data.json", "r") as f:
    data = json.load(f)


### Define the parameters

NumProducts = data["NumProducts"]

MaterialRequirement = data["MaterialRequirement"]

TimeRequirement = data["TimeRequirement"]

TotalMaterialsAvailable = data["TotalMaterialsAvailable"]

TotalLaborHoursAvailable = data["TotalLaborHoursAvailable"]

MinBasketballToFootballRatio = data["MinBasketballToFootballRatio"]

MinimumFootballs = data["MinimumFootballs"]


### Define the variables

Basketballs = model.addVar(vtype=GRB.INTEGER, lb=0, name="Basketballs")
Footballs = model.addVar(vtype=GRB.INTEGER, lb=0, name="Footballs")


### Define the constraints

model.addConstr(5 * Basketballs + 3 * Footballs <= TotalMaterialsAvailable)
model.addConstr(Basketballs + 2 * Footballs <= TotalLaborHoursAvailable)
model.addConstr(Basketballs >= MinBasketballToFootballRatio * Footballs)
model.addConstr(Footballs >= MinimumFootballs)


### Define the objective

model.setObjective(Basketballs + Footballs, GRB.MAXIMIZE)


### Optimize the model

model.optimize()


### Output optimal objective value

if model.status == GRB.OPTIMAL:
    print("Optimal Objective Value: ", model.objVal)
    with open("output_solution.txt", "w") as f:
        f.write(str(model.objVal))
else:
    with open("output_solution.txt", "w") as f:
        f.write(str(model.status))