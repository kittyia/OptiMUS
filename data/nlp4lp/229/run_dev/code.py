
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

NumberOfLimousines = model.addVar(vtype=GRB.INTEGER, name="NumberOfLimousines")

NumberOfBuses = model.addVar(vtype=GRB.INTEGER, name="NumberOfBuses")



### Define the constraints

model.addConstr(LimousineCapacity * NumberOfLimousines + BusCapacity * NumberOfBuses >= MinPeople)
model.addConstr(3 * NumberOfLimousines >= 7 * NumberOfBuses)
model.addConstr(NumberOfBuses >= 0)
model.addConstr(NumberOfLimousines >= 0)
model.addConstr(NumberOfBuses >= 0)


### Define the objective

model.setObjective(NumberOfLimousines + NumberOfBuses, GRB.MINIMIZE)


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
