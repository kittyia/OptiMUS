
import os
import numpy as np
import json 
from gurobipy import Model, GRB, quicksum


model = Model("OptimizationProblem")

with open("data.json", "r") as f:
    data = json.load(f)




### Define the parameters

NumSupplements = data["NumSupplements"] # shape: [], definition: Number of supplement types

NumNutrients = data["NumNutrients"] # shape: [], definition: Number of nutrient types

NutrientContent = data["NutrientContent"] # shape: ['NumSupplements', 'NumNutrients'], definition: Amount of nutrient j per pill of supplement i

MinRequirement = data["MinRequirement"] # shape: ['NumNutrients'], definition: Minimum required units of nutrient j

CostPerPill = data["CostPerPill"] # shape: ['NumSupplements'], definition: Cost per pill of supplement i



### Define the variables

NumPills = model.addVars(NumSupplements, vtype=GRB.INTEGER, name="NumPills")



### Define the constraints

model.addConstr(
    sum(NutrientContent[i][0] * NumPills[i] for i in range(NumSupplements)) 
    >= MinRequirement[0]
)
model.addConstr(NumPills[1] >= 0)
model.addConstr(NumPills[1] >= 0)


### Define the objective

model.setObjective(quicksum(CostPerPill[i] * NumPills[i] for i in range(NumSupplements)), GRB.MINIMIZE)


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
