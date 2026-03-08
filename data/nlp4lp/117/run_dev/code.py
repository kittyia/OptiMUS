
import os
import numpy as np
import json 
from gurobipy import Model, GRB, quicksum


model = Model("OptimizationProblem")

with open("data.json", "r") as f:
    data = json.load(f)




### Define the parameters

NumNutTypes = data["NumNutTypes"] # shape: [], definition: Number of different nut types

CaloriePerServing = data["CaloriePerServing"] # shape: ['NumNutTypes'], definition: Calories in one serving of each nut type

ProteinPerServing = data["ProteinPerServing"] # shape: ['NumNutTypes'], definition: Protein in one serving of each nut type

FatPerServing = data["FatPerServing"] # shape: ['NumNutTypes'], definition: Fat in one serving of each nut type

ServingRatioMultiplier = data["ServingRatioMultiplier"] # shape: [], definition: Minimum ratio of servings of almonds to cashews

CalorieRequirement = data["CalorieRequirement"] # shape: [], definition: Total calorie intake requirement

ProteinRequirement = data["ProteinRequirement"] # shape: [], definition: Total protein intake requirement



### Define the variables

ServingsOfAlmonds = model.addVar(vtype=GRB.CONTINUOUS, name="ServingsOfAlmonds")

ServingsOfCashews = model.addVar(vtype=GRB.CONTINUOUS, name="ServingsOfCashews")



### Define the constraints

model.addConstr(200 * ServingsOfAlmonds + 300 * ServingsOfCashews >= CalorieRequirement)
model.addConstr(20 * ServingsOfAlmonds + 25 * ServingsOfCashews >= ProteinRequirement)
model.addConstr(ServingsOfAlmonds >= ServingRatioMultiplier * ServingsOfCashews)
model.addConstr(ServingsOfAlmonds >= 0)
model.addConstr(ServingsOfCashews >= 0)


### Define the objective

model.setObjective(
    FatPerServing[0] * ServingsOfAlmonds + FatPerServing[1] * ServingsOfCashews,
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
