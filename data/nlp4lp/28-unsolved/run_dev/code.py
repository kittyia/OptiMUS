
import os
import numpy as np
import json 
from gurobipy import Model, GRB, quicksum


model = Model("OptimizationProblem")

with open("data.json", "r") as f:
    data = json.load(f)




### Define the parameters

NumVitamins = data["NumVitamins"] # shape: [], definition: NumVitamins

NumDrinks = data["NumDrinks"] # shape: [], definition: NumDrinks

MinRequirements = data["MinRequirements"] # shape: [4], definition: MinRequirements

MaxRequirements = data["MaxRequirements"] # shape: [4], definition: MaxRequirements

VitaminContent = data["VitaminContent"] # shape: [4, 2], definition: VitaminContent



### Define the variables

xA = model.addVar(vtype=GRB.CONTINUOUS, name="xA")

xB = model.addVar(vtype=GRB.CONTINUOUS, name="xB")



### Define the constraints

model.addConstr(8 * xA + 15 * xB >= 150)
model.addConstr(6 * xA + 2 * xB >= 300)
model.addConstr(10 * xA + 20 * xB <= 400)
model.addConstr(xA >= 0)
model.addConstr(xB >= 0)


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
