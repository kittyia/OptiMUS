
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

numberOfVans = model.addVar(vtype=GRB.INTEGER, name="numberOfVans")

numberOfCars = model.addVar(vtype=GRB.INTEGER, name="numberOfCars")



### Define the constraints

model.addConstr(VoterCapacityVan * numberOfVans + VoterCapacityCar * numberOfCars >= MinVoters)
model.addConstr(100 * numberOfVans <= MaxVanPercentage * (numberOfVans + numberOfCars))
model.addConstr(numberOfVans >= 0)
model.addConstr(numberOfCars >= 0)


### Define the objective

model.setObjective(numberOfCars, GRB.MINIMIZE)


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
