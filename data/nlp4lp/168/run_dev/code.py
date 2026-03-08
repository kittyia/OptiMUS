
import os
import numpy as np
import json 
from gurobipy import Model, GRB, quicksum


model = Model("OptimizationProblem")

with open("data.json", "r") as f:
    data = json.load(f)




### Define the parameters

BikeCapacity = data["BikeCapacity"] # shape: [], definition: Number of people each bike can transport

CarCapacity = data["CarCapacity"] # shape: [], definition: Number of people each car can transport

MaxCarPercentage = data["MaxCarPercentage"] # shape: [], definition: Maximum percentage of vehicles that can be cars

NumberOfPeople = data["NumberOfPeople"] # shape: [], definition: Total number of people to transport



### Define the variables

NumberOfBikes = model.addVar(vtype=GRB.INTEGER, name="NumberOfBikes")

NumberOfCars = model.addVar(vtype=GRB.INTEGER, name="NumberOfCars")



### Define the constraints

model.addConstr(BikeCapacity * NumberOfBikes + CarCapacity * NumberOfCars >= NumberOfPeople)
model.addConstr(3 * NumberOfCars <= 2 * NumberOfBikes)
model.addConstr(NumberOfBikes >= 0)
model.addConstr(NumberOfCars >= 0)
model.addConstr(NumberOfBikes >= 0)
model.addConstr(NumberOfCars >= 0)


### Define the objective

model.setObjective(NumberOfBikes, GRB.MINIMIZE)


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
