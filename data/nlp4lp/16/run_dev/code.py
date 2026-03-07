
import os
import numpy as np
import json 
from gurobipy import Model, GRB, quicksum


model = Model("OptimizationProblem")

with open("data.json", "r") as f:
    data = json.load(f)




### Define the parameters

RequiredZ1 = data["RequiredZ1"] # shape: [], definition: Minimum required daily amount of medicine Z1 in grams

RequiredD3 = data["RequiredD3"] # shape: [], definition: Minimum required daily amount of medicine D3 in grams

Z1PerZodiac = data["Z1PerZodiac"] # shape: [], definition: Amount of medicine Z1 in grams per pill of Zodiac

Z1PerSunny = data["Z1PerSunny"] # shape: [], definition: Amount of medicine Z1 in grams per pill of Sunny

D3PerZodiac = data["D3PerZodiac"] # shape: [], definition: Amount of medicine D3 in grams per pill of Zodiac

D3PerSunny = data["D3PerSunny"] # shape: [], definition: Amount of medicine D3 in grams per pill of Sunny

CostZodiac = data["CostZodiac"] # shape: [], definition: Cost per pill of Zodiac in dollars

CostSunny = data["CostSunny"] # shape: [], definition: Cost per pill of Sunny in dollars



### Define the variables

ZodiacPills = model.addVar(vtype=GRB.INTEGER, name="ZodiacPills")

SunnyPills = model.addVar(vtype=GRB.INTEGER, name="SunnyPills")



### Define the constraints

model.addConstr(Z1PerZodiac * ZodiacPills + Z1PerSunny * SunnyPills >= RequiredZ1)
model.addConstr(D3PerZodiac * ZodiacPills + D3PerSunny * SunnyPills >= RequiredD3)
model.addConstr(ZodiacPills >= 0)
model.addConstr(SunnyPills >= 0)


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
