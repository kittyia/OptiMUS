
import os
import numpy as np
import json 
from gurobipy import Model, GRB, quicksum


model = Model("OptimizationProblem")

with open("data.json", "r") as f:
    data = json.load(f)




### Define the parameters

NumOilTypes = data["NumOilTypes"] # shape: [], definition: Number of different types of car oils produced

NumSubstances = data["NumSubstances"] # shape: [], definition: Number of different substances used in the car oils

ProfitPerContainer = data["ProfitPerContainer"] # shape: ['NumOilTypes'], definition: Profit per container for each type of car oil

SubstanceAmountPerContainer = data["SubstanceAmountPerContainer"] # shape: ['NumSubstances', 'NumOilTypes'], definition: Amount of each substance required per container of each type of car oil

AvailableSubstances = data["AvailableSubstances"] # shape: ['NumSubstances'], definition: Available amount of each substance



### Define the variables

xOilMax = model.addVar(vtype=GRB.INTEGER, name="xOilMax")

xOilMaxPro = model.addVar(vtype=GRB.INTEGER, name="xOilMaxPro")



### Define the constraints

model.addConstr(43 * xOilMax + 4 * xOilMaxPro <= 346)
model.addConstr(56 * xOilMax + 45 * xOilMaxPro <= 1643)
model.addConstr(xOilMax >= 0)
model.addConstr(xOilMaxPro >= 0)


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
