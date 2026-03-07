
import os
import numpy as np
import json 
from gurobipy import Model, GRB, quicksum


model = Model("OptimizationProblem")

with open("data.json", "r") as f:
    data = json.load(f)




### Define the parameters

VanCapacity = data["VanCapacity"] # shape: [], definition: Capacity of a van in boxes per trip

TruckCapacity = data["TruckCapacity"] # shape: [], definition: Capacity of a truck in boxes per trip

VanCost = data["VanCost"] # shape: [], definition: Cost per van trip in dollars

TruckCost = data["TruckCost"] # shape: [], definition: Cost per truck trip in dollars

MinBoxes = data["MinBoxes"] # shape: [], definition: Minimum number of boxes to transport

Budget = data["Budget"] # shape: [], definition: Budget available in dollars



### Define the variables

VanTrips = model.addVar(vtype=GRB.INTEGER, name="VanTrips")

TruckTrips = model.addVar(vtype=GRB.INTEGER, name="TruckTrips")



### Define the constraints

model.addConstr(VanCapacity * VanTrips + TruckCapacity * TruckTrips >= MinBoxes)
model.addConstr(VanCost * VanTrips + TruckCost * TruckTrips <= Budget)
model.addConstr(VanTrips >= TruckTrips + 1)
model.addConstr(VanTrips >= 0)
model.addConstr(TruckTrips >= 0)


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
