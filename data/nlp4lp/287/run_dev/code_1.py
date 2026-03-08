import os
import numpy as np
import json
from gurobipy import Model, GRB, quicksum


model = Model("OptimizationProblem")

with open("data.json", "r") as f:
    data = json.load(f)


### Define the parameters

TotalInvestment = data["TotalInvestment"]
MinTelecomHealthcareRatio = data["MinTelecomHealthcareRatio"]
MaxTelecomInvestment = data["MaxTelecomInvestment"]
TelecomInterestRate = data["TelecomInterestRate"]
HealthcareInterestRate = data["HealthcareInterestRate"]


### Define the variables

TelecomInvestment = model.addVar(vtype=GRB.CONTINUOUS, lb=0, name="TelecomInvestment")
HealthcareInvestment = model.addVar(vtype=GRB.CONTINUOUS, lb=0, name="HealthcareInvestment")


### Define the constraints

model.addConstr(TelecomInvestment + HealthcareInvestment == TotalInvestment)
model.addConstr(TelecomInvestment >= MinTelecomHealthcareRatio * HealthcareInvestment)
model.addConstr(TelecomInvestment <= MaxTelecomInvestment)


### Define the objective

model.setObjective(
    TelecomInterestRate * TelecomInvestment +
    HealthcareInterestRate * HealthcareInvestment,
    GRB.MAXIMIZE
)


### Optimize the model

model.optimize()


### Output results safely

if model.status == GRB.OPTIMAL:
    print("Optimal Objective Value: ", model.ObjVal)
    with open("output_solution.txt", "w") as f:
        f.write(str(model.ObjVal))
else:
    print("Optimization was not successful. Status code:", model.status)
    with open("output_solution.txt", "w") as f:
        f.write(str(model.status))