
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

ContainersProduced = model.addVars(NumOilTypes, vtype=GRB.INTEGER, name="ContainersProduced")



### Define the constraints

model.addConstr(
    sum(SubstanceAmountPerContainer[0][t] * ContainersProduced[t] 
        for t in range(NumOilTypes)) 
    <= AvailableSubstances[0]
)
model.addConstr(
    sum(SubstanceAmountPerContainer[2][j] * ContainersProduced[j] 
        for j in range(NumOilTypes)) 
    <= AvailableSubstances[2]
)
model.addConstr(
    sum(SubstanceAmountPerContainer[2][j] * ContainersProduced[j] 
        for j in range(NumOilTypes)) 
    <= AvailableSubstances[2]
)
for i in range(NumOilTypes):
    model.addConstr(ContainersProduced[i] >= 0)
for i in range(NumOilTypes):
    model.addConstr(ContainersProduced[i] >= 0)


### Define the objective

model.setObjective(
    quicksum(ProfitPerContainer[i] * ContainersProduced[i] for i in range(NumOilTypes)),
    GRB.MAXIMIZE
)


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
