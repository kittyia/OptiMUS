
import os
import numpy as np
import json 
from gurobipy import Model, GRB, quicksum


model = Model("OptimizationProblem")

with open("data.json", "r") as f:
    data = json.load(f)




### Define the parameters

TotalHorsesAvailable = data["TotalHorsesAvailable"] # shape: [], definition: Total number of horses available for transportation

HorsesPerMediumCart = data["HorsesPerMediumCart"] # shape: [], definition: Number of horses required to operate one medium sized cart

HorsesPerLargeCart = data["HorsesPerLargeCart"] # shape: [], definition: Number of horses required to operate one large sized cart

CapacityMediumCart = data["CapacityMediumCart"] # shape: [], definition: Rice carrying capacity of one medium sized cart in kilograms

CapacityLargeCart = data["CapacityLargeCart"] # shape: [], definition: Rice carrying capacity of one large sized cart in kilograms

MediumToLargeCartRatio = data["MediumToLargeCartRatio"] # shape: [], definition: Required ratio of medium sized carts to large sized carts

MinMediumCarts = data["MinMediumCarts"] # shape: [], definition: Minimum number of medium sized carts required

MinLargeCarts = data["MinLargeCarts"] # shape: [], definition: Minimum number of large sized carts required



### Define the variables

mediumCarts = model.addVar(vtype=GRB.INTEGER, name="mediumCarts")

largeCarts = model.addVar(vtype=GRB.INTEGER, name="largeCarts")



### Define the constraints

model.addConstr(HorsesPerMediumCart * mediumCarts + HorsesPerLargeCart * largeCarts <= TotalHorsesAvailable)
model.addConstr(mediumCarts == MediumToLargeCartRatio * largeCarts)
model.addConstr(largeCarts >= MinLargeCarts)
# mediumCarts and largeCarts are defined as integer variables (vtype=GRB.INTEGER),
# so no additional constraint is required here.


### Define the objective

model.setObjective(
    CapacityMediumCart * mediumCarts + CapacityLargeCart * largeCarts,
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
