
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

NumberOfCarts = model.addVar(vtype=GRB.INTEGER, name="NumberOfCarts")

NumberOfTrolleys = model.addVar(vtype=GRB.INTEGER, name="NumberOfTrolleys")



### Define the constraints

model.addConstr(CartTransportRate * NumberOfCarts + TrolleyTransportRate * NumberOfTrolleys >= DeliveryRate)
model.addConstr(NumberOfTrolleys >= MinTrolleys)
model.addConstr(
    TrolleyTransportRate * NumberOfTrolleys
    <= (MaxTrolleyTransportPercentage / 100.0) * 
       (CartTransportRate * NumberOfCarts + TrolleyTransportRate * NumberOfTrolleys)
)
model.addConstr(NumberOfCarts >= 0)
model.addConstr(NumberOfCarts >= 0)
model.addConstr(NumberOfTrolleys >= 0)


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
