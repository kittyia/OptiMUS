
import os
import numpy as np
import json 
from gurobipy import Model, GRB, quicksum


model = Model("OptimizationProblem")

with open("data.json", "r") as f:
    data = json.load(f)




### Define the parameters

CartTransportRate = data["CartTransportRate"] # shape: [], definition: Equipment transport rate of carts in kilograms per minute

CartWorkersRequired = data["CartWorkersRequired"] # shape: [], definition: Number of workers required per cart

TrolleyTransportRate = data["TrolleyTransportRate"] # shape: [], definition: Equipment transport rate of trolleys in kilograms per minute

TrolleyWorkersRequired = data["TrolleyWorkersRequired"] # shape: [], definition: Number of workers required per trolley

MinTrolleys = data["MinTrolleys"] # shape: [], definition: Minimum number of trolleys to be used

MaxTrolleyTransportPercentage = data["MaxTrolleyTransportPercentage"] # shape: [], definition: Maximum percentage of transportation that can use trolleys

DeliveryRate = data["DeliveryRate"] # shape: [], definition: Delivery rate of equipment in kilograms per minute



### Define the variables

Carts = model.addVar(vtype=GRB.INTEGER, name="Carts")

Trolleys = model.addVar(vtype=GRB.INTEGER, name="Trolleys")



### Define the constraints

model.addConstr(CartTransportRate * Carts + TrolleyTransportRate * Trolleys >= DeliveryRate)
model.addConstr(Trolleys >= MinTrolleys)
model.addConstr(Carts >= 2.1 * Trolleys)
model.addConstr(Carts >= 0)
model.addConstr(Carts >= 0)
model.addConstr(Trolleys >= 0)


### Define the objective

model.setObjective(CartWorkersRequired * Carts + TrolleyWorkersRequired * Trolleys, GRB.MINIMIZE)


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
