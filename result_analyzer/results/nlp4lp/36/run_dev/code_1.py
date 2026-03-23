import os
import numpy as np
import json
from gurobipy import Model, GRB, quicksum


model = Model("OptimizationProblem")

with open("data.json", "r") as f:
    data = json.load(f)


### Define the parameters

VegetableVitamins = data["VegetableVitamins"]
VegetableMinerals = data["VegetableMinerals"]
FruitVitamins = data["FruitVitamins"]
FruitMinerals = data["FruitMinerals"]
MinimumVitamins = data["MinimumVitamins"]
MinimumMinerals = data["MinimumMinerals"]
VegetableCost = data["VegetableCost"]
FruitCost = data["FruitCost"]


### Define the variables

VegetableServings = model.addVar(vtype=GRB.CONTINUOUS, name="VegetableServings")
FruitServings = model.addVar(vtype=GRB.CONTINUOUS, name="FruitServings")


### Define the constraints

model.addConstr(
    VegetableVitamins * VegetableServings + 
    FruitVitamins * FruitServings >= MinimumVitamins,
    name="VitaminRequirement"
)

model.addConstr(
    VegetableMinerals * VegetableServings + 
    FruitMinerals * FruitServings >= MinimumMinerals,
    name="MineralRequirement"
)

model.addConstr(VegetableServings >= 0, name="NonNegVegetables")
model.addConstr(FruitServings >= 0, name="NonNegFruits")


### Define the objective

model.setObjective(
    VegetableCost * VegetableServings + 
    FruitCost * FruitServings,
    GRB.MINIMIZE
)


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
``