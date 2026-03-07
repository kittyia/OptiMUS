
import os
import numpy as np
import json 
from gurobipy import Model, GRB, quicksum


model = Model("OptimizationProblem")

with open("data.json", "r") as f:
    data = json.load(f)




### Define the parameters

CapacityLargeUnit = data["CapacityLargeUnit"] # shape: [], definition: Number of people that one large mobile production unit can hold

ParkingLargeUnit = data["ParkingLargeUnit"] # shape: [], definition: Number of parking spots occupied by one large mobile production unit

CapacitySmallUnit = data["CapacitySmallUnit"] # shape: [], definition: Number of people that one small mobile production unit can hold

ParkingSmallUnit = data["ParkingSmallUnit"] # shape: [], definition: Number of parking spots occupied by one small mobile production unit

MinSmallUnits = data["MinSmallUnits"] # shape: [], definition: Minimum number of small mobile production units required

MinLargeUnitProportion = data["MinLargeUnitProportion"] # shape: [], definition: Minimum proportion of large mobile production units relative to total vehicles

TotalPeople = data["TotalPeople"] # shape: [], definition: Total number of people that need to be transported



### Define the variables

NumberOfLargeUnits = model.addVar(vtype=GRB.INTEGER, name="NumberOfLargeUnits")

NumberOfSmallUnits = model.addVar(vtype=GRB.INTEGER, name="NumberOfSmallUnits")



### Define the constraints

model.addConstr(CapacityLargeUnit * NumberOfLargeUnits + CapacitySmallUnit * NumberOfSmallUnits >= TotalPeople)
model.addConstr(NumberOfSmallUnits >= MinSmallUnits)
model.addConstr(NumberOfLargeUnits >= 3 * NumberOfSmallUnits)
model.addConstr(NumberOfLargeUnits >= 0)
model.addConstr(NumberOfSmallUnits >= 0)


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
