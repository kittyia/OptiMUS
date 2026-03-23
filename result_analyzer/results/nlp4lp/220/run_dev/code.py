
import os
import numpy as np
import json 
from gurobipy import Model, GRB, quicksum


model = Model("OptimizationProblem")

with open("data.json", "r") as f:
    data = json.load(f)




### Define the parameters

TimeToEffectCalcium = data["TimeToEffectCalcium"] # shape: [], definition: Time it takes for a calcium pill to be effective

TimeToEffectVitaminD = data["TimeToEffectVitaminD"] # shape: [], definition: Time it takes for a vitamin D pill to be effective

MinTotalPills = data["MinTotalPills"] # shape: [], definition: Minimum total number of pills to be taken in a month

MinVitaminDPills = data["MinVitaminDPills"] # shape: [], definition: Minimum number of vitamin D pills to be taken in a month



### Define the variables

CalciumPills = model.addVar(vtype=GRB.INTEGER, name="CalciumPills")

VitaminDPills = model.addVar(vtype=GRB.INTEGER, name="VitaminDPills")



### Define the constraints

model.addConstr(CalciumPills + VitaminDPills >= MinTotalPills)
model.addConstr(VitaminDPills >= MinVitaminDPills)
model.addConstr(CalciumPills >= VitaminDPills + 1)
# No additional constraints are required here because integrality
# is enforced when defining the variables using vtype=GRB.INTEGER.


### Define the objective

model.setObjective(TimeToEffectCalcium * CalciumPills + TimeToEffectVitaminD * VitaminDPills, GRB.MINIMIZE)


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
