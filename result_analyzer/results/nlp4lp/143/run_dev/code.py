
import os
import numpy as np
import json 
from gurobipy import Model, GRB, quicksum


model = Model("OptimizationProblem")

with open("data.json", "r") as f:
    data = json.load(f)




### Define the parameters

OldVanCapacity = data["OldVanCapacity"] # shape: [], definition: Capacity of an old van in soda bottles

NewVanCapacity = data["NewVanCapacity"] # shape: [], definition: Capacity of a new van in soda bottles

OldVanPollution = data["OldVanPollution"] # shape: [], definition: Pollution produced by an old van in units

NewVanPollution = data["NewVanPollution"] # shape: [], definition: Pollution produced by a new van in units

MinimumBottles = data["MinimumBottles"] # shape: [], definition: Minimum number of soda bottles that need to be sent

MaximumNewVans = data["MaximumNewVans"] # shape: [], definition: Maximum number of new vans that can be used



### Define the variables

OldVans = model.addVar(vtype=GRB.INTEGER, name="OldVans")

NewVans = model.addVar(vtype=GRB.INTEGER, name="NewVans")



### Define the constraints

model.addConstr(OldVanCapacity * OldVans + NewVanCapacity * NewVans >= MinimumBottles)
model.addConstr(NewVans <= MaximumNewVans)
model.addConstr(OldVans >= 0)
model.addConstr(NewVans >= 0)


### Define the objective

model.setObjective(OldVanPollution * OldVans + NewVanPollution * NewVans, GRB.MINIMIZE)


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
