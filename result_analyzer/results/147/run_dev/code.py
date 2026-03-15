
import os
import numpy as np
import json 
from gurobipy import Model, GRB, quicksum


model = Model("OptimizationProblem")

with open("data.json", "r") as f:
    data = json.load(f)




### Define the parameters

ContainerCapacity = data["ContainerCapacity"] # shape: [], definition: Number of units of oil each container can hold

TruckCapacity = data["TruckCapacity"] # shape: [], definition: Number of units of oil each truck can hold

TruckToContainerRatio = data["TruckToContainerRatio"] # shape: [], definition: Maximum allowed ratio of number of trucks to number of containers

MinimumOilSent = data["MinimumOilSent"] # shape: [], definition: Minimum number of units of oil that need to be sent to the port

MinimumContainers = data["MinimumContainers"] # shape: [], definition: Minimum number of containers that need to be used



### Define the variables

NumberOfContainers = model.addVar(vtype=GRB.INTEGER, name="NumberOfContainers")

NumberOfTrucks = model.addVar(vtype=GRB.INTEGER, name="NumberOfTrucks")



### Define the constraints

model.addConstr(ContainerCapacity * NumberOfContainers + TruckCapacity * NumberOfTrucks >= MinimumOilSent)
model.addConstr(NumberOfTrucks <= TruckToContainerRatio * NumberOfContainers)
model.addConstr(NumberOfContainers >= MinimumContainers)
model.addConstr(NumberOfTrucks >= 0)
model.addConstr(NumberOfContainers >= 0)
model.addConstr(NumberOfTrucks >= 0)


### Define the objective

model.setObjective(NumberOfContainers + NumberOfTrucks, GRB.MINIMIZE)


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
