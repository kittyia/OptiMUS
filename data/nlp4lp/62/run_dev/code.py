
import os
import numpy as np
import json 
from gurobipy import Model, GRB, quicksum


model = Model("OptimizationProblem")

with open("data.json", "r") as f:
    data = json.load(f)




### Define the parameters

CustomersSmall = data["CustomersSmall"] # shape: [], definition: Number of customers a small branch can serve per day

TellersSmall = data["TellersSmall"] # shape: [], definition: Number of tellers required by a small branch

CustomersLarge = data["CustomersLarge"] # shape: [], definition: Number of customers a large branch can serve per day

TellersLarge = data["TellersLarge"] # shape: [], definition: Number of tellers required by a large branch

TotalTellers = data["TotalTellers"] # shape: [], definition: Total number of available bank tellers

MinCustomers = data["MinCustomers"] # shape: [], definition: Minimum number of customers that need to be served per day



### Define the variables

SmallBranches = model.addVar(vtype=GRB.INTEGER, name="SmallBranches")

LargeBranches = model.addVar(vtype=GRB.INTEGER, name="LargeBranches")



### Define the constraints

model.addConstr(TellersSmall * SmallBranches + TellersLarge * LargeBranches <= TotalTellers)
model.addConstr(CustomersSmall * SmallBranches + CustomersLarge * LargeBranches >= MinCustomers)
model.addConstr(SmallBranches >= 0)
model.addConstr(LargeBranches >= 0)


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
