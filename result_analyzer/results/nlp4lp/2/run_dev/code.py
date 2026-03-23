
import os
import numpy as np
import json 
from gurobipy import Model, GRB, quicksum


model = Model("OptimizationProblem")

with open("data.json", "r") as f:
    data = json.load(f)




### Define the parameters

NumSandwichTypes = data["NumSandwichTypes"] # shape: [], definition: Number of different sandwich types

NumIngredients = data["NumIngredients"] # shape: [], definition: Number of different ingredients

Required = data["Required"] # shape: ['NumIngredients', 'NumSandwichTypes'], definition: Amount of ingredient j required to produce one unit of sandwich i

TotalAvailable = data["TotalAvailable"] # shape: ['NumIngredients'], definition: Total availability of ingredient j

ProfitPerSandwich = data["ProfitPerSandwich"] # shape: ['NumSandwichTypes'], definition: Profit per unit of sandwich i



### Define the variables

RegularSandwiches = model.addVar(vtype=GRB.INTEGER, name="RegularSandwiches")

SpecialSandwiches = model.addVar(vtype=GRB.INTEGER, name="SpecialSandwiches")



### Define the constraints

model.addConstr(2 * RegularSandwiches + 3 * SpecialSandwiches <= 40)
model.addConstr(RegularSandwiches >= 0)
model.addConstr(SpecialSandwiches >= 0)


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
