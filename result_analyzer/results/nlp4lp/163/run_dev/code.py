
import os
import numpy as np
import json 
from gurobipy import Model, GRB, quicksum


model = Model("OptimizationProblem")

with open("data.json", "r") as f:
    data = json.load(f)




### Define the parameters

VanCapacity = data["VanCapacity"] # shape: [], definition: Number of kids a van can take

VanPollution = data["VanPollution"] # shape: [], definition: Pollution produced by one van

MinibusCapacity = data["MinibusCapacity"] # shape: [], definition: Number of kids a minibus can take

MinibusPollution = data["MinibusPollution"] # shape: [], definition: Pollution produced by one minibus

MinimumNumberOfKids = data["MinimumNumberOfKids"] # shape: [], definition: Minimum number of kids that need to go to school

MaximumNumberOfMinibuses = data["MaximumNumberOfMinibuses"] # shape: [], definition: Maximum number of minibuses that can be used



### Define the variables

NumberOfVans = model.addVar(vtype=GRB.INTEGER, name="NumberOfVans")

NumberOfMinibuses = model.addVar(vtype=GRB.INTEGER, name="NumberOfMinibuses")



### Define the constraints

model.addConstr(VanCapacity * NumberOfVans + MinibusCapacity * NumberOfMinibuses >= MinimumNumberOfKids)
model.addConstr(NumberOfMinibuses <= MaximumNumberOfMinibuses)
model.addConstr(NumberOfVans >= NumberOfMinibuses + 1)
model.addConstr(NumberOfVans >= 0)
model.addConstr(NumberOfMinibuses >= 0)


### Define the objective

model.setObjective(VanPollution * NumberOfVans + MinibusPollution * NumberOfMinibuses, GRB.MINIMIZE)


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
