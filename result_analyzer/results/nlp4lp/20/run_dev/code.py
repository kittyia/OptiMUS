
import os
import numpy as np
import json 
from gurobipy import Model, GRB, quicksum


model = Model("OptimizationProblem")

with open("data.json", "r") as f:
    data = json.load(f)




### Define the parameters

TotalSpace = data["TotalSpace"] # shape: [], definition: Total available space in square feet

Budget = data["Budget"] # shape: [], definition: Maximum allowed budget in dollars

LaborHoursAvailable = data["LaborHoursAvailable"] # shape: [], definition: Maximum available labor hours

NumberOfProducts = data["NumberOfProducts"] # shape: [], definition: Number of products produced

LaborRequiredPerSqFt = data["LaborRequiredPerSqFt"] # shape: ['NumberOfProducts'], definition: Labor hours required per square foot for each product

CostPerSqFt = data["CostPerSqFt"] # shape: ['NumberOfProducts'], definition: Cost per square foot for each product

RevenuePerSqFt = data["RevenuePerSqFt"] # shape: ['NumberOfProducts'], definition: Net revenue per square foot for each product



### Define the variables

SpaceAllocated = model.addVars(NumberOfProducts, vtype=GRB.CONTINUOUS, name="SpaceAllocated")



### Define the constraints

model.addConstr(
    sum(SpaceAllocated[p] for p in range(NumberOfProducts)) <= TotalSpace
)
for i in range(NumberOfProducts):
    model.addConstr(SpaceAllocated[i] >= 0)


### Define the objective

model.setObjective(quicksum(RevenuePerSqFt[i] * SpaceAllocated[i] for i in range(NumberOfProducts)), GRB.MAXIMIZE)


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
