
import os
import numpy as np
import json 
from gurobipy import Model, GRB, quicksum


model = Model("OptimizationProblem")

with open("data.json", "r") as f:
    data = json.load(f)




### Define the parameters

CustomerInteractionsCart = data["CustomerInteractionsCart"] # shape: [], definition: Customer interactions per cart delivery server per hour

CustomerInteractionsHand = data["CustomerInteractionsHand"] # shape: [], definition: Customer interactions per hand delivery server per hour

RefillsCart = data["RefillsCart"] # shape: [], definition: Number of refills per cart delivery server per hour

RefillsHand = data["RefillsHand"] # shape: [], definition: Number of refills per hand delivery server per hour

MinFractionCart = data["MinFractionCart"] # shape: [], definition: Minimum fraction of delivery shifts that must be by cart

MinServersHand = data["MinServersHand"] # shape: [], definition: Minimum number of servers delivering by hand

TargetCustomerInteractions = data["TargetCustomerInteractions"] # shape: [], definition: Target total number of customer interactions per hour



### Define the variables

NumberCartServers = model.addVar(vtype=GRB.INTEGER, name="NumberCartServers")

NumberHandServers = model.addVar(vtype=GRB.INTEGER, name="NumberHandServers")



### Define the constraints

model.addConstr(
    CustomerInteractionsCart * NumberCartServers
    + CustomerInteractionsHand * NumberHandServers
    >= TargetCustomerInteractions
)
model.addConstr(NumberCartServers >= MinFractionCart * (NumberCartServers + NumberHandServers))
model.addConstr(NumberHandServers >= MinServersHand)
model.addConstr(NumberCartServers >= 0)
model.addConstr(NumberHandServers >= 0)


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
