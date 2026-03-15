
import os
import numpy as np
import json 
from gurobipy import Model, GRB, quicksum


model = Model("OptimizationProblem")

with open("data.json", "r") as f:
    data = json.load(f)




### Define the parameters

GolfCartCapacity = data["GolfCartCapacity"] # shape: [], definition: Capacity of a golf cart

PullCartCapacity = data["PullCartCapacity"] # shape: [], definition: Capacity of a pull cart

MaxGolfCartPercentage = data["MaxGolfCartPercentage"] # shape: [], definition: Maximum percentage of carts that can be golf carts

MinGuests = data["MinGuests"] # shape: [], definition: Minimum number of guests to transport



### Define the variables

GolfCarts = model.addVar(vtype=GRB.INTEGER, name="GolfCarts")

PullCarts = model.addVar(vtype=GRB.INTEGER, name="PullCarts")



### Define the constraints

model.addConstr(GolfCartCapacity * GolfCarts + PullCartCapacity * PullCarts >= MinGuests)
model.addConstr(GolfCarts <= MaxGolfCartPercentage * (GolfCarts + PullCarts))
model.addConstr(GolfCarts >= 0)
model.addConstr(PullCarts >= 0)
model.addConstr(GolfCarts >= 0)
model.addConstr(PullCarts >= 0)


### Define the objective

model.setObjective(GolfCarts + PullCarts, GRB.MINIMIZE)


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
