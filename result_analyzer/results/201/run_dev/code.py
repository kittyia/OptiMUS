
import os
import numpy as np
import json 
from gurobipy import Model, GRB, quicksum


model = Model("OptimizationProblem")

with open("data.json", "r") as f:
    data = json.load(f)




### Define the parameters

MinLaminateDemand = data["MinLaminateDemand"] # shape: [], definition: Minimum weekly demand for laminate planks

MinCarpetDemand = data["MinCarpetDemand"] # shape: [], definition: Minimum weekly demand for carpets

MinTotalShipping = data["MinTotalShipping"] # shape: [], definition: Minimum total weekly shipping requirement

MaxLaminateProduction = data["MaxLaminateProduction"] # shape: [], definition: Maximum weekly production capacity for laminate planks

MaxCarpetProduction = data["MaxCarpetProduction"] # shape: [], definition: Maximum weekly production capacity for carpets

LaminateProfitPerSqFt = data["LaminateProfitPerSqFt"] # shape: [], definition: Profit per square foot for laminate planks

CarpetProfitPerSqFt = data["CarpetProfitPerSqFt"] # shape: [], definition: Profit per square foot for carpets



### Define the variables

LaminateProduction = model.addVar(vtype=GRB.CONTINUOUS, name="LaminateProduction")

CarpetProduction = model.addVar(vtype=GRB.CONTINUOUS, name="CarpetProduction")



### Define the constraints

model.addConstr(LaminateProduction >= MinLaminateDemand)
model.addConstr(CarpetProduction >= MinCarpetDemand)
model.addConstr(LaminateProduction + CarpetProduction >= MinTotalShipping)
model.addConstr(LaminateProduction <= MaxLaminateProduction)
model.addConstr(CarpetProduction <= MaxCarpetProduction)


### Define the objective

model.setObjective(
    LaminateProfitPerSqFt * LaminateProduction +
    CarpetProfitPerSqFt * CarpetProduction,
    GRB.MAXIMIZE
)


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
