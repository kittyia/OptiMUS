
import os
import numpy as np
import json 
from gurobipy import Model, GRB, quicksum


model = Model("OptimizationProblem")

with open("data.json", "r") as f:
    data = json.load(f)




### Define the parameters

NumDeskTypes = data["NumDeskTypes"] # shape: [], definition: Number of desk types

Price = data["Price"] # shape: ['NumDeskTypes'], definition: Cost of each desk type

Space = data["Space"] # shape: ['NumDeskTypes'], definition: Space occupied by each desk type

Seats = data["Seats"] # shape: ['NumDeskTypes'], definition: Seating capacity of each desk type

MaxBudget = data["MaxBudget"] # shape: [], definition: Maximum budget available

MaxSpace = data["MaxSpace"] # shape: [], definition: Maximum office space for desks



### Define the variables

NumDesks = model.addVars(NumDeskTypes, vtype=GRB.INTEGER, name="NumDesks")



### Define the constraints

model.addConstr(sum(Price[i] * NumDesks[i] for i in range(NumDeskTypes)) <= MaxBudget)
model.addConstr(
    sum(Space[i] * NumDesks[i] for i in range(NumDeskTypes)) <= MaxSpace
)
for i in range(NumDeskTypes):  
    model.addConstr(NumDesks[i] >= 0)


### Define the objective

model.setObjective(quicksum(Seats[i] * NumDesks[i] for i in range(NumDeskTypes)), GRB.MAXIMIZE)


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
