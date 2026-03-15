
import os
import numpy as np
import json 
from gurobipy import Model, GRB, quicksum


model = Model("OptimizationProblem")

with open("data.json", "r") as f:
    data = json.load(f)




### Define the parameters

MinMathWorkbooks = data["MinMathWorkbooks"] # shape: [], definition: Minimum number of math workbooks to produce

MinEnglishWorkbooks = data["MinEnglishWorkbooks"] # shape: [], definition: Minimum number of English workbooks to produce

MaxMathWorkbooks = data["MaxMathWorkbooks"] # shape: [], definition: Maximum number of math workbooks to produce

MaxEnglishWorkbooks = data["MaxEnglishWorkbooks"] # shape: [], definition: Maximum number of English workbooks to produce

MinTotalWorkbooks = data["MinTotalWorkbooks"] # shape: [], definition: Minimum total number of workbooks to produce

ProfitMathWorkbook = data["ProfitMathWorkbook"] # shape: [], definition: Profit per math workbook

ProfitEnglishWorkbook = data["ProfitEnglishWorkbook"] # shape: [], definition: Profit per English workbook



### Define the variables

MathWorkbooks = model.addVar(vtype=GRB.INTEGER, name="MathWorkbooks")

EnglishWorkbooks = model.addVar(vtype=GRB.INTEGER, name="EnglishWorkbooks")



### Define the constraints

model.addConstr(MathWorkbooks >= MinMathWorkbooks)
model.addConstr(MathWorkbooks <= MaxMathWorkbooks)
model.addConstr(EnglishWorkbooks >= MinEnglishWorkbooks)
model.addConstr(EnglishWorkbooks <= MaxEnglishWorkbooks)
model.addConstr(MathWorkbooks + EnglishWorkbooks >= MinTotalWorkbooks)


### Define the objective

model.setObjective(ProfitMathWorkbook * MathWorkbooks + ProfitEnglishWorkbook * EnglishWorkbooks, GRB.MAXIMIZE)


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
