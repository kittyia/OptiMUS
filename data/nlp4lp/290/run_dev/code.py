
import os
import numpy as np
import json 
from gurobipy import Model, GRB, quicksum


model = Model("OptimizationProblem")

with open("data.json", "r") as f:
    data = json.load(f)




### Define the parameters

TotalInvestment = data["TotalInvestment"] # shape: [], definition: Total amount of money available to invest

ClothingToTechRatio = data["ClothingToTechRatio"] # shape: [], definition: Minimum ratio of clothing investment to tech investment

MaxTechInvestment = data["MaxTechInvestment"] # shape: [], definition: Maximum investment allowed in tech company

ClothingInterestRate = data["ClothingInterestRate"] # shape: [], definition: Interest rate earned from clothing company investment

TechInterestRate = data["TechInterestRate"] # shape: [], definition: Interest rate earned from tech company investment



### Define the variables

ClothingInvestment = model.addVar(vtype=GRB.CONTINUOUS, name="ClothingInvestment")

TechInvestment = model.addVar(vtype=GRB.CONTINUOUS, name="TechInvestment")



### Define the constraints

model.addConstr(ClothingInvestment + TechInvestment == TotalInvestment)
model.addConstr(ClothingInvestment >= ClothingToTechRatio * TechInvestment)
model.addConstr(TechInvestment <= MaxTechInvestment)
model.addConstr(TechInvestment >= 0)


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
