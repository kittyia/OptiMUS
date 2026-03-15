
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

NumberCart = model.addVar(vtype=GRB.INTEGER, name="NumberCart")

NumberHand = model.addVar(vtype=GRB.INTEGER, name="NumberHand")



### Define the constraints

model.addConstr(
    CustomerInteractionsCart * NumberCart + CustomerInteractionsHand * NumberHand
    >= TargetCustomerInteractions
)
model.addConstr(NumberCart >= MinFractionCart * (NumberCart + NumberHand))
model.addConstr(NumberHand >= MinServersHand)


### Define the objective

model.setObjective(RefillsCart * NumberCart + RefillsHand * NumberHand, GRB.MINIMIZE)


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
