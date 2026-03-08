
import os
import numpy as np
import json 
from gurobipy import Model, GRB, quicksum


model = Model("OptimizationProblem")

with open("data.json", "r") as f:
    data = json.load(f)




### Define the parameters

ProfitPerRegularTaco = data["ProfitPerRegularTaco"] # shape: [], definition: Profit per regular taco

ProfitPerDeluxeTaco = data["ProfitPerDeluxeTaco"] # shape: [], definition: Profit per deluxe taco

MaxDemandRegularTacos = data["MaxDemandRegularTacos"] # shape: [], definition: Maximum demand for regular tacos

MaxDemandDeluxeTacos = data["MaxDemandDeluxeTacos"] # shape: [], definition: Maximum demand for deluxe tacos

MaxTotalSupplyTacos = data["MaxTotalSupplyTacos"] # shape: [], definition: Maximum total supply of tacos



### Define the variables

x1 = model.addVar(vtype=GRB.INTEGER, name="x1")

x2 = model.addVar(vtype=GRB.INTEGER, name="x2")



### Define the constraints

model.addConstr(x1 >= 0)
model.addConstr(x1 <= MaxDemandRegularTacos)
model.addConstr(x2 >= 0)
model.addConstr(x2 <= MaxDemandDeluxeTacos)
model.addConstr(x1 + x2 <= MaxTotalSupplyTacos)


### Define the objective

model.setObjective(ProfitPerRegularTaco * x1 + ProfitPerDeluxeTaco * x2, GRB.MAXIMIZE)


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
