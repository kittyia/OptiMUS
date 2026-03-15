
import os
import numpy as np
import json 
from gurobipy import Model, GRB, quicksum


model = Model("OptimizationProblem")

with open("data.json", "r") as f:
    data = json.load(f)




### Define the parameters

ScooterCapacity = data["ScooterCapacity"] # shape: [], definition: Capacity of a scooter in number of people

RickshawCapacity = data["RickshawCapacity"] # shape: [], definition: Capacity of a rickshaw in number of people

MaxRickshawPercentage = data["MaxRickshawPercentage"] # shape: [], definition: Maximum percentage of vehicles that can be rickshaws

NumVisitors = data["NumVisitors"] # shape: [], definition: Number of visitors to transport



### Define the variables

numScooters = model.addVar(vtype=GRB.INTEGER, name="numScooters")

numRickshaws = model.addVar(vtype=GRB.INTEGER, name="numRickshaws")



### Define the constraints

model.addConstr(ScooterCapacity * numScooters + RickshawCapacity * numRickshaws >= NumVisitors)
model.addConstr(3 * numRickshaws <= 2 * numScooters)
model.addConstr(numScooters >= 0)
model.addConstr(numRickshaws >= 0)
model.addConstr(numScooters >= 0)
model.addConstr(numRickshaws >= 0)


### Define the objective

model.setObjective(numScooters, GRB.MINIMIZE)


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
