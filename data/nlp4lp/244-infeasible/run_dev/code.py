
import os
import numpy as np
import json 
from gurobipy import Model, GRB, quicksum


model = Model("OptimizationProblem")

with open("data.json", "r") as f:
    data = json.load(f)




### Define the parameters

LargeBagCapacity = data["LargeBagCapacity"] # shape: [], definition: The capacity of a large bag in kilograms

LargeBagEnergy = data["LargeBagEnergy"] # shape: [], definition: The energy required to transport a large bag

TinyBagCapacity = data["TinyBagCapacity"] # shape: [], definition: The capacity of a tiny bag in kilograms

TinyBagEnergy = data["TinyBagEnergy"] # shape: [], definition: The energy required to transport a tiny bag

TotalEnergy = data["TotalEnergy"] # shape: [], definition: Total available energy for distribution

RatioLargeToTiny = data["RatioLargeToTiny"] # shape: [], definition: The ratio of large bags to tiny bags

MinTinyBags = data["MinTinyBags"] # shape: [], definition: Minimum number of tiny bags required



### Define the variables

LargeBags = model.addVar(vtype=GRB.INTEGER, name="LargeBags")

TinyBags = model.addVar(vtype=GRB.INTEGER, name="TinyBags")



### Define the constraints

model.addConstr(LargeBagEnergy * LargeBags + TinyBagEnergy * TinyBags <= TotalEnergy)
model.addConstr(LargeBags == 2 * TinyBags)
model.addConstr(TinyBags >= MinTinyBags)
model.addConstr(LargeBags >= 0)
model.addConstr(TinyBags >= 0)


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
