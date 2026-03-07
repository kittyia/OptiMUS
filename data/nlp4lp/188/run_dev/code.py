
import os
import numpy as np
import json 
from gurobipy import Model, GRB, quicksum


model = Model("OptimizationProblem")

with open("data.json", "r") as f:
    data = json.load(f)




### Define the parameters

VoterCapacityVan = data["VoterCapacityVan"] # shape: [], definition: Number of voters a van can carry

VoterCapacityCar = data["VoterCapacityCar"] # shape: [], definition: Number of voters a car can carry

MinVoters = data["MinVoters"] # shape: [], definition: Minimum number of voters to transport

MaxVanPercentage = data["MaxVanPercentage"] # shape: [], definition: Maximum percentage of vehicles that can be vans



### Define the variables

NumberOfVans = model.addVar(vtype=GRB.INTEGER, name="NumberOfVans")

NumberOfCars = model.addVar(vtype=GRB.INTEGER, name="NumberOfCars")



### Define the constraints

model.addConstr(VoterCapacityVan * NumberOfVans + VoterCapacityCar * NumberOfCars >= MinVoters)
model.addConstr(7 * NumberOfVans <= 3 * NumberOfCars])
model.addConstr(NumberOfVans >= 0)
model.addConstr(NumberOfCars >= 0)
model.addConstr(NumberOfVans >= 0)
model.addConstr(NumberOfCars >= 0)


### Define the objective

model.setObjective(NumberOfCars, GRB.MINIMIZE)


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
