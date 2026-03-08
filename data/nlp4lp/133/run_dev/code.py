
import os
import numpy as np
import json 
from gurobipy import Model, GRB, quicksum


model = Model("OptimizationProblem")

with open("data.json", "r") as f:
    data = json.load(f)




### Define the parameters

TotalMedicinalIngredients = data["TotalMedicinalIngredients"] # shape: [], definition: Total units of medicinal ingredients available to produce pills

NumPillTypes = data["NumPillTypes"] # shape: [], definition: Number of different pill types

RequiredMedicinal = data["RequiredMedicinal"] # shape: ['NumPillTypes'], definition: Units of medicinal ingredients required to produce one unit of pill type i

RequiredFiller = data["RequiredFiller"] # shape: ['NumPillTypes'], definition: Units of filler required to produce one unit of pill type i

MinimumPills = data["MinimumPills"] # shape: ['NumPillTypes'], definition: Minimum number of pills that must be produced for pill type i

MinimumProportion = data["MinimumProportion"] # shape: ['NumPillTypes'], definition: Minimum proportion of total pills that must be of pill type i



### Define the variables

NumPills = model.addVars(NumPillTypes, vtype=GRB.INTEGER, name="NumPills")



### Define the constraints

model.addConstr(
    sum(RequiredMedicinal[i] * NumPills[i] for i in range(NumPillTypes)) 
    <= TotalMedicinalIngredients
)
model.addConstr(NumPills[0] >= 100)
model.addConstr(NumPills[1] >= 0.6 * (NumPills[0] + NumPills[1]))


### Define the objective

model.setObjective(quicksum(RequiredFiller[i] * NumPills[i] for i in range(NumPillTypes)), GRB.MINIMIZE)


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
