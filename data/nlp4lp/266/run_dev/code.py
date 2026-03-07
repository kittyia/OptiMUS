
import os
import numpy as np
import json 
from gurobipy import Model, GRB, quicksum


model = Model("OptimizationProblem")

with open("data.json", "r") as f:
    data = json.load(f)




### Define the parameters

FiberSpinach = data["FiberSpinach"] # shape: [], definition: Number of units of fiber in one cup of spinach

IronSpinach = data["IronSpinach"] # shape: [], definition: Amount of iron (mg) in one cup of spinach

CaloriesSpinach = data["CaloriesSpinach"] # shape: [], definition: Number of calories in one cup of spinach

FiberSoybeans = data["FiberSoybeans"] # shape: [], definition: Number of units of fiber in one cup of soybeans

IronSoybeans = data["IronSoybeans"] # shape: [], definition: Amount of iron (mg) in one cup of soybeans

CaloriesSoybeans = data["CaloriesSoybeans"] # shape: [], definition: Number of calories in one cup of soybeans

MinFiber = data["MinFiber"] # shape: [], definition: Minimum total units of fiber required

MinIron = data["MinIron"] # shape: [], definition: Minimum total amount of iron required (mg)



### Define the variables

SpinachCups = model.addVar(vtype=GRB.CONTINUOUS, name="SpinachCups")

SoybeanCups = model.addVar(vtype=GRB.CONTINUOUS, name="SoybeanCups")



### Define the constraints

model.addConstr(FiberSpinach * SpinachCups + FiberSoybeans * SoybeanCups >= MinFiber)
model.addConstr(IronSpinach * SpinachCups + IronSoybeans * SoybeanCups >= MinIron)
model.addConstr(SpinachCups >= SoybeanCups))
model.addConstr(SpinachCups >= 0)
model.addConstr(SoybeanCups >= 0)


### Define the objective

model.setObjective(CaloriesSpinach * SpinachCups + CaloriesSoybeans * SoybeanCups, GRB.MAXIMIZE)


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
