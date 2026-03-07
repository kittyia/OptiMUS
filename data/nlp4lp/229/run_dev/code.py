
import os
import numpy as np
import json 
from gurobipy import Model, GRB, quicksum


model = Model("OptimizationProblem")

with open("data.json", "r") as f:
    data = json.load(f)




### Define the parameters

LimousineCapacity = data["LimousineCapacity"] # shape: [], definition: Number of people a limousine can carry

BusCapacity = data["BusCapacity"] # shape: [], definition: Number of people a bus can carry

MinPeople = data["MinPeople"] # shape: [], definition: Minimum number of people to transport

MinLimousineFraction = data["MinLimousineFraction"] # shape: [], definition: Minimum fraction of vehicles that must be limousines



### Define the variables

numLimousines = model.addVar(vtype=GRB.INTEGER, name="numLimousines")

numBuses = model.addVar(vtype=GRB.INTEGER, name="numBuses")



### Define the constraints

model.addConstr(LimousineCapacity * numLimousines + BusCapacity * numBuses >= MinPeople)
model.addConstr(3 * numLimousines >= 7 * numBuses)
model.addConstr(numLimousines >= 0)
model.addConstr(numBuses >= 0)


### Define the objective

model.setObjective(numLimousines + numBuses, GRB.MINIMIZE)


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
