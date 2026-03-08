import os
import numpy as np
import json
from gurobipy import Model, GRB, quicksum


model = Model("OptimizationProblem")

with open("data.json", "r") as f:
    data = json.load(f)


### Define the parameters

MinVitamins = data["MinVitamins"]
MinFiber = data["MinFiber"]

VitaminsPerSalad = data["VitaminsPerSalad"]
VitaminsPerFruitBowl = data["VitaminsPerFruitBowl"]

FiberPerSalad = data["FiberPerSalad"]
FiberPerFruitBowl = data["FiberPerFruitBowl"]

PotassiumPerSalad = data["PotassiumPerSalad"]
PotassiumPerFruitBowl = data["PotassiumPerFruitBowl"]

MaxFruitBowlFraction = data["MaxFruitBowlFraction"]


### Define the variables

Salads = model.addVar(vtype=GRB.CONTINUOUS, name="Salads", lb=0)
FruitBowls = model.addVar(vtype=GRB.CONTINUOUS, name="FruitBowls", lb=0)


### Define the constraints

model.addConstr(
    VitaminsPerSalad * Salads + VitaminsPerFruitBowl * FruitBowls >= MinVitamins,
    name="VitaminRequirement"
)

model.addConstr(
    FiberPerSalad * Salads + FiberPerFruitBowl * FruitBowls >= MinFiber,
    name="FiberRequirement"
)

model.addConstr(
    FruitBowls <= MaxFruitBowlFraction * (Salads + FruitBowls),
    name="FruitFractionLimit"
)


### Define the objective

model.setObjective(
    PotassiumPerSalad * Salads + PotassiumPerFruitBowl * FruitBowls,
    GRB.MAXIMIZE
)


### Optimize the model

model.optimize()


### Output optimal objective value

if model.status == GRB.OPTIMAL:
    print("Optimal Objective Value:", model.ObjVal)
    with open("output_solution.txt", "w") as f:
        f.write(str(model.ObjVal))
else:
    print("Optimization was not successful. Status code:", model.status)
    with open("output_solution.txt", "w") as f:
        f.write(str(model.status))