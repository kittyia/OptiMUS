
import os
import numpy as np
import json 
from gurobipy import Model, GRB, quicksum


model = Model("OptimizationProblem")

with open("data.json", "r") as f:
    data = json.load(f)




### Define the parameters

TotalFarmArea = data["TotalFarmArea"] # shape: [], definition: Total area of the farm in acres

TotalWateringBudget = data["TotalWateringBudget"] # shape: [], definition: Total budget available for watering in dollars

TotalAvailableLabor = data["TotalAvailableLabor"] # shape: [], definition: Total available labor in days

NumCrops = data["NumCrops"] # shape: [], definition: Number of different crops to be planted

LaborPerAcre = data["LaborPerAcre"] # shape: ['NumCrops'], definition: Amount of labor required per acre for each crop in days

WateringCostPerAcre = data["WateringCostPerAcre"] # shape: ['NumCrops'], definition: Watering cost per acre for each crop in dollars

ProfitPerAcre = data["ProfitPerAcre"] # shape: ['NumCrops'], definition: Profit per acre for each crop in dollars



### Define the variables

AcresPlanted = model.addVars(NumCrops, vtype=GRB.CONTINUOUS, name="AcresPlanted")



### Define the constraints

model.addConstr(sum(AcresPlanted[c] for c in range(NumCrops)) <= TotalFarmArea)
model.addConstr(
    sum(WateringCostPerAcre[i] * AcresPlanted[i] for i in range(NumCrops))
    <= TotalWateringBudget
)
model.addConstr(
    sum(LaborPerAcre[i] * AcresPlanted[i] for i in range(NumCrops)) 
    <= TotalAvailableLabor
)
for c in range(NumCrops):
    model.addConstr(AcresPlanted[c] >= 0)


### Define the objective

model.setObjective(quicksum(ProfitPerAcre[i] * AcresPlanted[i] for i in range(NumCrops)), GRB.MAXIMIZE)


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
