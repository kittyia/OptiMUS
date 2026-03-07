
import os
import numpy as np
import json 
from gurobipy import Model, GRB, quicksum


model = Model("OptimizationProblem")

with open("data.json", "r") as f:
    data = json.load(f)




### Define the parameters

TotalInvestment = data["TotalInvestment"] # shape: [], definition: Total amount of money available for investment

MinTelecomHealthcareRatio = data["MinTelecomHealthcareRatio"] # shape: [], definition: Minimum ratio of telecom investment to healthcare investment

MaxTelecomInvestment = data["MaxTelecomInvestment"] # shape: [], definition: Maximum investment allowed in telecom

TelecomInterestRate = data["TelecomInterestRate"] # shape: [], definition: Interest rate earned from telecom investments

HealthcareInterestRate = data["HealthcareInterestRate"] # shape: [], definition: Interest rate earned from healthcare investments



### Define the variables

TelecomInvestment = model.addVar(vtype=GRB.CONTINUOUS, name="TelecomInvestment")

HealthcareInvestment = model.addVar(vtype=GRB.CONTINUOUS, name="HealthcareInvestment")



### Define the constraints

model.addConstr(TelecomInvestment + HealthcareInvestment == TotalInvestment)
model.addConstr(TelecomInvestment >= MinTelecomHealthcareRatio * HealthcareInvestment)
model.addConstr(TelecomInvestment <= MaxTelecomInvestment)
model.addConstr(HealthcareInvestment >= 0)


### Define the objective

model.setObjective(
    TelecomInterestRate * TelecomInvestment + 
    HealthcareInterestRate * HealthcareInvestment,
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
