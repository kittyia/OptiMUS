import os
import numpy as np
import json
from gurobipy import Model, GRB, quicksum


model = Model("OptimizationProblem")

with open("data.json", "r") as f:
    data = json.load(f)


### Define the parameters

FiberSpinach = data["FiberSpinach"]
IronSpinach = data["IronSpinach"]
CaloriesSpinach = data["CaloriesSpinach"]

FiberSoybeans = data["FiberSoybeans"]
IronSoybeans = data["IronSoybeans"]
CaloriesSoybeans = data["CaloriesSoybeans"]

MinFiber = data["MinFiber"]
MinIron = data["MinIron"]


### Define the variables

SpinachCups = model.addVar(vtype=GRB.CONTINUOUS, name="SpinachCups")
SoybeanCups = model.addVar(vtype=GRB.CONTINUOUS, name="SoybeanCups")


### Define the constraints

model.addConstr(FiberSpinach * SpinachCups + FiberSoybeans * SoybeanCups >= MinFiber)
model.addConstr(IronSpinach * SpinachCups + IronSoybeans * SoybeanCups >= MinIron)
model.addConstr(SpinachCups >= SoybeanCups)
model.addConstr(SpinachCups >= 0)
model.addConstr(SoybeanCups >= 0)


### Define the objective

model.setObjective(
    CaloriesSpinach * SpinachCups + CaloriesSoybeans * SoybeanCups,
    GRB.MAXIMIZE
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