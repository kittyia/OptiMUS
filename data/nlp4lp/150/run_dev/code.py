
import os
import numpy as np
import json 
from gurobipy import Model, GRB, quicksum


model = Model("OptimizationProblem")

with open("data.json", "r") as f:
    data = json.load(f)




### Define the parameters

FlowersPerSmallBouquet = data["FlowersPerSmallBouquet"] # shape: [], definition: Number of flowers in a small bouquet

FlowersPerLargeBouquet = data["FlowersPerLargeBouquet"] # shape: [], definition: Number of flowers in a large bouquet

MaxSmallBouquets = data["MaxSmallBouquets"] # shape: [], definition: Maximum number of small bouquets that can be transported

MaxLargeBouquets = data["MaxLargeBouquets"] # shape: [], definition: Maximum number of large bouquets that can be transported

MaxTotalBouquets = data["MaxTotalBouquets"] # shape: [], definition: Maximum total number of bouquets that can be transported

MinLargeBouquets = data["MinLargeBouquets"] # shape: [], definition: Minimum number of large bouquets that must be transported

MinSmallToLargeRatio = data["MinSmallToLargeRatio"] # shape: [], definition: Minimum ratio of small bouquets to large bouquets



### Define the variables

SmallBouquets = model.addVar(vtype=GRB.INTEGER, name="SmallBouquets")

LargeBouquets = model.addVar(vtype=GRB.INTEGER, name="LargeBouquets")



### Define the constraints

model.addConstr(SmallBouquets + LargeBouquets <= MaxTotalBouquets)
model.addConstr(LargeBouquets >= MinLargeBouquets)
model.addConstr(SmallBouquets >= MinSmallToLargeRatio * LargeBouquets)


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
