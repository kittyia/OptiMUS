
import os
import numpy as np
import json 
from gurobipy import Model, GRB, quicksum


model = Model("OptimizationProblem")

with open("data.json", "r") as f:
    data = json.load(f)




### Define the parameters

TotalInvestment = data["TotalInvestment"] # shape: [], definition: Total amount available for investment

MaxInvestmentApartments = data["MaxInvestmentApartments"] # shape: [], definition: Maximum amount that can be invested in apartments

MinInvestmentRatio = data["MinInvestmentRatio"] # shape: [], definition: Minimum ratio of investment in apartments to investment in townhouses

ReturnRateApartments = data["ReturnRateApartments"] # shape: [], definition: Return on investment rate for apartments

ReturnRateTownhouses = data["ReturnRateTownhouses"] # shape: [], definition: Return on investment rate for townhouses



### Define the variables

InvestmentApartments = model.addVar(vtype=GRB.CONTINUOUS, name="InvestmentApartments")

InvestmentTownhouses = model.addVar(vtype=GRB.CONTINUOUS, name="InvestmentTownhouses")



### Define the constraints

model.addConstr(InvestmentApartments + InvestmentTownhouses == TotalInvestment)
model.addConstr(InvestmentApartments <= MaxInvestmentApartments)
model.addConstr(InvestmentApartments >= MinInvestmentRatio * InvestmentTownhouses)


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
