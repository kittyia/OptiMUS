
import os
import numpy as np
import json 
from gurobipy import Model, GRB, quicksum


model = Model("OptimizationProblem")

with open("data.json", "r") as f:
    data = json.load(f)




### Define the parameters

LargeShipCapacity = data["LargeShipCapacity"] # shape: [], definition: Number of containers a large ship can carry

SmallShipCapacity = data["SmallShipCapacity"] # shape: [], definition: Number of containers a small ship can carry

RequiredContainers = data["RequiredContainers"] # shape: [], definition: Minimum number of containers to transport



### Define the variables

LargeShips = model.addVar(vtype=GRB.INTEGER, name="LargeShips")

SmallShips = model.addVar(vtype=GRB.INTEGER, name="SmallShips")



### Define the constraints

model.addConstr(LargeShipCapacity * LargeShips + SmallShipCapacity * SmallShips >= RequiredContainers)
model.addConstr(LargeShips <= SmallShips)
model.addConstr(LargeShips >= 0)
model.addConstr(SmallShips >= 0)


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
