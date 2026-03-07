
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

NumberOfScooters = model.addVar(vtype=GRB.INTEGER, name="NumberOfScooters")

NumberOfBikes = model.addVar(vtype=GRB.INTEGER, name="NumberOfBikes")



### Define the constraints

model.addConstr(
    DesignHoursPerScooter * NumberOfScooters +
    DesignHoursPerBike * NumberOfBikes
    <= TotalDesignHoursAvailable
)
model.addConstr(EngineeringHoursPerScooter * NumberOfScooters + EngineeringHoursPerBike * NumberOfBikes <= TotalEngineeringHoursAvailable)
model.addConstr(NumberOfScooters >= 0)
model.addConstr(NumberOfBikes >= 0)


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
