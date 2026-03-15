
import os
import numpy as np
import json 
from gurobipy import Model, GRB, quicksum


model = Model("OptimizationProblem")

with open("data.json", "r") as f:
    data = json.load(f)




### Define the parameters

BreadPerLight = data["BreadPerLight"] # shape: [], definition: Number of slices of bread required to make one light grilled cheese sandwich

CheesePerLight = data["CheesePerLight"] # shape: [], definition: Number of slices of cheese required to make one light grilled cheese sandwich

BreadPerHeavy = data["BreadPerHeavy"] # shape: [], definition: Number of slices of bread required to make one heavy grilled cheese sandwich

CheesePerHeavy = data["CheesePerHeavy"] # shape: [], definition: Number of slices of cheese required to make one heavy grilled cheese sandwich

MinHeavyToLightRatio = data["MinHeavyToLightRatio"] # shape: [], definition: Minimum ratio of heavy grilled cheese sandwiches to light grilled cheese sandwiches

TotalBread = data["TotalBread"] # shape: [], definition: Total number of slices of bread available

TotalCheese = data["TotalCheese"] # shape: [], definition: Total number of slices of cheese available

TimePerLight = data["TimePerLight"] # shape: [], definition: Time in minutes to make one light grilled cheese sandwich

TimePerHeavy = data["TimePerHeavy"] # shape: [], definition: Time in minutes to make one heavy grilled cheese sandwich



### Define the variables

Light = model.addVar(vtype=GRB.INTEGER, name="Light")

Heavy = model.addVar(vtype=GRB.INTEGER, name="Heavy")



### Define the constraints

model.addConstr(BreadPerLight * Light + BreadPerHeavy * Heavy <= TotalBread)
model.addConstr(Heavy >= MinHeavyToLightRatio * Light)
model.addConstr(Light >= 0)
model.addConstr(Heavy >= 0)


### Define the objective

del.setObjective(TimePerLight * Light + TimePerHeavy * Heavy, GRB.MINIMIZE


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
