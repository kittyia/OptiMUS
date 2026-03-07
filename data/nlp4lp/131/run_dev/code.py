
import os
import numpy as np
import json 
from gurobipy import Model, GRB, quicksum


model = Model("OptimizationProblem")

with open("data.json", "r") as f:
    data = json.load(f)




### Define the parameters

ProteinTurkey = data["ProteinTurkey"] # shape: [], definition: Amount of protein in one turkey dinner

CarbsTurkey = data["CarbsTurkey"] # shape: [], definition: Amount of carbohydrates in one turkey dinner

FatTurkey = data["FatTurkey"] # shape: [], definition: Amount of fat in one turkey dinner

ProteinTuna = data["ProteinTuna"] # shape: [], definition: Amount of protein in one tuna salad sandwich

CarbsTuna = data["CarbsTuna"] # shape: [], definition: Amount of carbohydrates in one tuna salad sandwich

FatTuna = data["FatTuna"] # shape: [], definition: Amount of fat in one tuna salad sandwich

MinProtein = data["MinProtein"] # shape: [], definition: Minimum required total protein

MinCarbs = data["MinCarbs"] # shape: [], definition: Minimum required total carbohydrates

MaxTurkeyFraction = data["MaxTurkeyFraction"] # shape: [], definition: Maximum fraction of meals that can be turkey dinners



### Define the variables

TurkeyMeals = model.addVar(vtype=GRB.INTEGER, name="TurkeyMeals")

TunaMeals = model.addVar(vtype=GRB.INTEGER, name="TunaMeals")



### Define the constraints

model.addConstr(ProteinTurkey * TurkeyMeals + ProteinTuna * TunaMeals >= MinProtein)
model.addConstr(CarbsTurkey * TurkeyMeals + CarbsTuna * TunaMeals >= MinCarbs)
model.addConstr(TurkeyMeals <= MaxTurkeyFraction * (TurkeyMeals + TunaMeals))
model.addConstr(TurkeyMeals >= 0)
model.addConstr(TunaMeals >= 0)


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
