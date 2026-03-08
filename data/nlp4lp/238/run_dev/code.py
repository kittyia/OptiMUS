
import os
import numpy as np
import json 
from gurobipy import Model, GRB, quicksum


model = Model("OptimizationProblem")

with open("data.json", "r") as f:
    data = json.load(f)




### Define the parameters

MinVitamins = data["MinVitamins"] # shape: [], definition: Minimum required units of vitamins per staff

MinFiber = data["MinFiber"] # shape: [], definition: Minimum required units of fiber per staff

VitaminsPerSalad = data["VitaminsPerSalad"] # shape: [], definition: Units of vitamins per salad

VitaminsPerFruitBowl = data["VitaminsPerFruitBowl"] # shape: [], definition: Units of vitamins per fruit bowl

FiberPerSalad = data["FiberPerSalad"] # shape: [], definition: Units of fiber per salad

FiberPerFruitBowl = data["FiberPerFruitBowl"] # shape: [], definition: Units of fiber per fruit bowl

PotassiumPerSalad = data["PotassiumPerSalad"] # shape: [], definition: Units of potassium per salad

PotassiumPerFruitBowl = data["PotassiumPerFruitBowl"] # shape: [], definition: Units of potassium per fruit bowl

MaxFruitBowlFraction = data["MaxFruitBowlFraction"] # shape: [], definition: Maximum fraction of meals that can be fruit bowls



### Define the variables

Salads = model.addVar(vtype=GRB.CONTINUOUS, name="Salads")

FruitBowls = model.addVar(vtype=GRB.CONTINUOUS, name="FruitBowls")



### Define the constraints

model.addConstr(VitaminsPerSalad * Salads + VitaminsPerFruitBowl * FruitBowls >= MinVitamins)
model.addConstr(FiberPerSalad * Salads + FiberPerFruitBowl * FruitBowls >= MinFiber)
model.addConstr(FruitBowls <= MaxFruitBowlFraction * (Salads + FruitBowls))
model.addConstr(Salads >= 0)
model.addConstr(FruitBowls >= 0)


### Define the objective

model.setObjective(PotassiumPerSalad * Salads + PotassiumPerFruitBowl * FruitBowls, GRB.MAXIMIZE)


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
