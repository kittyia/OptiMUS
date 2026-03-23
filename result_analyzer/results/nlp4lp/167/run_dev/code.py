
import os
import numpy as np
import json 
from gurobipy import Model, GRB, quicksum


model = Model("OptimizationProblem")

with open("data.json", "r") as f:
    data = json.load(f)




### Define the parameters

TractorCapacity = data["TractorCapacity"] # shape: [], definition: Capacity of one tractor in kilograms

CarCapacity = data["CarCapacity"] # shape: [], definition: Capacity of one car in kilograms

MinimumCarMultiplier = data["MinimumCarMultiplier"] # shape: [], definition: Minimum multiplier for the number of cars relative to tractors

MinimumCornToSend = data["MinimumCornToSend"] # shape: [], definition: Minimum total amount of corn to send in kilograms



### Define the variables

NumTractors = model.addVar(vtype=GRB.INTEGER, name="NumTractors")

NumCars = model.addVar(vtype=GRB.INTEGER, name="NumCars")



### Define the constraints

model.addConstr(TractorCapacity * NumTractors + CarCapacity * NumCars >= MinimumCornToSend)
model.addConstr(NumCars >= MinimumCarMultiplier * NumTractors)
model.addConstr(NumTractors >= 0)
model.addConstr(NumCars >= 0)


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
