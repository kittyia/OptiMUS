
import os
import numpy as np
import json 
from gurobipy import Model, GRB, quicksum


model = Model("OptimizationProblem")

with open("data.json", "r") as f:
    data = json.load(f)




### Define the parameters

AlloyQuantity = data["AlloyQuantity"] # shape: [], definition: Quantity of alloy to produce

NumMetals = data["NumMetals"] # shape: [], definition: Number of metals

NumAlloys = data["NumAlloys"] # shape: [], definition: Number of alloys

Target = data["Target"] # shape: ['NumMetals'], definition: Quantity of target components in the alloy

Ratio = data["Ratio"] # shape: ['NumAlloys', 'NumMetals'], definition: Ratio of each component k in the alloy m

Price = data["Price"] # shape: ['NumAlloys'], definition: Price of each alloy k



### Define the variables

amount = model.addVars(NumAlloys, vtype=GRB.CONTINUOUS, name="amount")



### Define the constraints

for m in range(NumMetals):
    model.addConstr(
        sum(Ratio[k][m] * amount[k] for k in range(NumAlloys)) == Target[m]
    )
for k in range(NumAlloys):
    model.addConstr(amount[k] >= 0)


### Define the objective

model.setObjective(quicksum(Price[k] * amount[k] for k in range(NumAlloys)), GRB.MINIMIZE)


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
