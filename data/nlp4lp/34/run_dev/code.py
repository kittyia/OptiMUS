
import os
import numpy as np
import json 
from gurobipy import Model, GRB, quicksum


model = Model("OptimizationProblem")

with open("data.json", "r") as f:
    data = json.load(f)




### Define the parameters

ProfitPerScooter = data["ProfitPerScooter"] # shape: [], definition: Profit per scooter

ProfitPerBike = data["ProfitPerBike"] # shape: [], definition: Profit per bike

DesignHoursPerScooter = data["DesignHoursPerScooter"] # shape: [], definition: Design hours required per scooter

DesignHoursPerBike = data["DesignHoursPerBike"] # shape: [], definition: Design hours required per bike

EngineeringHoursPerScooter = data["EngineeringHoursPerScooter"] # shape: [], definition: Engineering hours required per scooter

EngineeringHoursPerBike = data["EngineeringHoursPerBike"] # shape: [], definition: Engineering hours required per bike

TotalDesignHoursAvailable = data["TotalDesignHoursAvailable"] # shape: [], definition: Total design hours available per month

TotalEngineeringHoursAvailable = data["TotalEngineeringHoursAvailable"] # shape: [], definition: Total engineering hours available per month



### Define the variables

NumScooters = model.addVar(vtype=GRB.INTEGER, name="NumScooters")

NumBikes = model.addVar(vtype=GRB.INTEGER, name="NumBikes")



### Define the constraints

model.addConstr(DesignHoursPerScooter * NumScooters + DesignHoursPerBike * NumBikes <= TotalDesignHoursAvailable)
model.addConstr(
    EngineeringHoursPerScooter * NumScooters +
    EngineeringHoursPerBike * NumBikes
    <= TotalEngineeringHoursAvailable
)
model.addConstr(NumScooters >= 0)
model.addConstr(NumBikes >= 0)
model.addConstr(NumScooters >= 0)
model.addConstr(NumBikes >= 0)


### Define the objective

model.setObjective(ProfitPerScooter * NumScooters + ProfitPerBike * NumBikes, GRB.MAXIMIZE)


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
