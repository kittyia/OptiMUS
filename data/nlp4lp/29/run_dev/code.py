
import os
import numpy as np
import json 
from gurobipy import Model, GRB, quicksum


model = Model("OptimizationProblem")

with open("data.json", "r") as f:
    data = json.load(f)




### Define the parameters

MinGallonsChocolate = data["MinGallonsChocolate"] # shape: [], definition: Minimum gallons of chocolate ice cream to produce per week

MinGallonsVanilla = data["MinGallonsVanilla"] # shape: [], definition: Minimum gallons of vanilla ice cream to produce per week

MaxGallonsChocolate = data["MaxGallonsChocolate"] # shape: [], definition: Maximum gallons of chocolate ice cream to produce per week

MaxGallonsVanilla = data["MaxGallonsVanilla"] # shape: [], definition: Maximum gallons of vanilla ice cream to produce per week

ProductionTimeChocolate = data["ProductionTimeChocolate"] # shape: [], definition: Production time in hours to produce one gallon of chocolate ice cream

ProductionTimeVanilla = data["ProductionTimeVanilla"] # shape: [], definition: Production time in hours to produce one gallon of vanilla ice cream

TotalProductionHours = data["TotalProductionHours"] # shape: [], definition: Total production hours available per week

WorkersNeededChocolate = data["WorkersNeededChocolate"] # shape: [], definition: Number of workers required to operate production of chocolate ice cream

WorkersNeededVanilla = data["WorkersNeededVanilla"] # shape: [], definition: Number of workers required to operate production of vanilla ice cream

MinTotalWorkers = data["MinTotalWorkers"] # shape: [], definition: Minimum total number of workers required

ProfitChocolate = data["ProfitChocolate"] # shape: [], definition: Profit per gallon of chocolate ice cream

ProfitVanilla = data["ProfitVanilla"] # shape: [], definition: Profit per gallon of vanilla ice cream



### Define the variables

GallonsChocolate = model.addVar(vtype=GRB.CONTINUOUS, name="GallonsChocolate")

GallonsVanilla = model.addVar(vtype=GRB.CONTINUOUS, name="GallonsVanilla")



### Define the constraints

model.addConstr(GallonsChocolate >= MinGallonsChocolate)
model.addConstr(GallonsChocolate <= MaxGallonsChocolate)
model.addConstr(GallonsVanilla >= MinGallonsVanilla)
model.addConstr(GallonsVanilla <= MaxGallonsVanilla)
model.addConstr(ProductionTimeChocolate * GallonsChocolate + ProductionTimeVanilla * GallonsVanilla <= TotalProductionHours)
model.addConstr(WorkersNeededChocolate * GallonsChocolate + WorkersNeededVanilla * GallonsVanilla >= MinTotalWorkers)


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
