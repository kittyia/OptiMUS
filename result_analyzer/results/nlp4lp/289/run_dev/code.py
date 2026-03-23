
import os
import numpy as np
import json 
from gurobipy import Model, GRB, quicksum


model = Model("OptimizationProblem")

with open("data.json", "r") as f:
    data = json.load(f)




### Define the parameters

MaxWiredProduction = data["MaxWiredProduction"] # shape: [], definition: Maximum wired headphones produced per day

MaxWirelessProduction = data["MaxWirelessProduction"] # shape: [], definition: Maximum wireless headphones produced per day

MaxTestingCapacity = data["MaxTestingCapacity"] # shape: [], definition: Maximum capacity of shared audio testing machine per day

ProfitWired = data["ProfitWired"] # shape: [], definition: Profit per wired headphone

ProfitWireless = data["ProfitWireless"] # shape: [], definition: Profit per wireless headphone



### Define the variables

WiredProduction = model.addVar(vtype=GRB.INTEGER, name="WiredProduction")

WirelessProduction = model.addVar(vtype=GRB.INTEGER, name="WirelessProduction")



### Define the constraints

model.addConstr(WiredProduction <= MaxWiredProduction)
model.addConstr(WirelessProduction <= MaxWirelessProduction)
model.addConstr(WiredProduction + WirelessProduction <= MaxTestingCapacity)
model.addConstr(WiredProduction >= 0)
model.addConstr(WirelessProduction >= 0)


### Define the objective

model.setObjective(ProfitWired * WiredProduction + ProfitWireless * WirelessProduction, GRB.MAXIMIZE)


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
