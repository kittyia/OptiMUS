
import os
import numpy as np
import json 
from gurobipy import Model, GRB, quicksum


model = Model("OptimizationProblem")

with open("data.json", "r") as f:
    data = json.load(f)




### Define the parameters

SmallBusCapacity = data["SmallBusCapacity"] # shape: [], definition: Capacity of a small bus

LargeBusCapacity = data["LargeBusCapacity"] # shape: [], definition: Capacity of a large bus

MinimumStudents = data["MinimumStudents"] # shape: [], definition: Minimum number of students to transport

MaxLargeBusPercentage = data["MaxLargeBusPercentage"] # shape: [], definition: Maximum percentage of buses that can be large buses



### Define the variables

smallBuses = model.addVar(vtype=GRB.INTEGER, name="smallBuses")

largeBuses = model.addVar(vtype=GRB.INTEGER, name="largeBuses")



### Define the constraints

model.addConstr(SmallBusCapacity * smallBuses + LargeBusCapacity * largeBuses >= MinimumStudents)
model.addConstr(largeBuses <= MaxLargeBusPercentage * (smallBuses + largeBuses))
model.addConstr(smallBuses >= 0)
model.addConstr(largeBuses >= 0)
model.addConstr(smallBuses >= 0)
model.addConstr(largeBuses >= 0)


### Define the objective

model.setObjective(smallBuses + largeBuses, GRB.MINIMIZE)


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
