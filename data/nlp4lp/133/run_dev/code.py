
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

LargePills = model.addVar(vtype=GRB.INTEGER, name="LargePills")

SmallPills = model.addVar(vtype=GRB.INTEGER, name="SmallPills")



### Define the constraints

model.addConstr(3 * LargePills + 2 * SmallPills <= TotalMedicinalIngredients)
model.addConstr(LargePills >= 100)
model.addConstr(SmallPills >= 0.6 * (LargePills + SmallPills))


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
