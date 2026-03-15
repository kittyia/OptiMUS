
import os
import numpy as np
import json 
from gurobipy import Model, GRB, quicksum


model = Model("OptimizationProblem")

with open("data.json", "r") as f:
    data = json.load(f)




### Define the parameters

MaxSpendingBudget = data["MaxSpendingBudget"] # shape: [], definition: The maximum amount the owner can spend on mangos and guavas

CostMango = data["CostMango"] # shape: [], definition: The cost to purchase one mango

CostGuava = data["CostGuava"] # shape: [], definition: The cost to purchase one guava

ProfitMango = data["ProfitMango"] # shape: [], definition: The profit earned from selling one mango

ProfitGuava = data["ProfitGuava"] # shape: [], definition: The profit earned from selling one guava

MinMangosSold = data["MinMangosSold"] # shape: [], definition: The minimum number of mangos sold each month

MaxMangosSold = data["MaxMangosSold"] # shape: [], definition: The maximum number of mangos sold each month

MaxGuavaToMangoRatio = data["MaxGuavaToMangoRatio"] # shape: [], definition: The maximum proportion of guavas sold relative to mangos sold



### Define the variables

MangoSold = model.addVar(vtype=GRB.INTEGER, name="MangoSold")

GuavaSold = model.addVar(vtype=GRB.INTEGER, name="GuavaSold")



### Define the constraints

model.addConstr(CostMango * MangoSold + CostGuava * GuavaSold <= MaxSpendingBudget)
model.addConstr(MangoSold >= MinMangosSold)
model.addConstr(MangoSold <= MaxMangosSold)
model.addConstr(GuavaSold <= MaxGuavaToMangoRatio * MangoSold)
model.addConstr(GuavaSold >= 0)


### Define the objective

model.setObjective(ProfitMango * MangoSold + ProfitGuava * GuavaSold, GRB.MAXIMIZE)


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
