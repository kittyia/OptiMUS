import os
import numpy as np
import json
from gurobipy import Model, GRB, quicksum


model = Model("OptimizationProblem")

with open("data.json", "r") as f:
    data = json.load(f)


# Define the parameters
LowPowerCoolingCapacity = data["LowPowerCoolingCapacity"]
LowPowerElectricityUsage = data["LowPowerElectricityUsage"]
HighPowerCoolingCapacity = data["HighPowerCoolingCapacity"]
HighPowerElectricityUsage = data["HighPowerElectricityUsage"]
MaxLowPowerPercentage = data["MaxLowPowerPercentage"]
MinHighPowerModels = data["MinHighPowerModels"]
TotalCoolingRequired = data["TotalCoolingRequired"]
TotalElectricityAvailable = data["TotalElectricityAvailable"]


# Define the variables
LowPowerUnits = model.addVar(vtype=GRB.INTEGER, name="LowPowerUnits")
HighPowerUnits = model.addVar(vtype=GRB.INTEGER, name="HighPowerUnits")


# Define the constraints
model.addConstr(
    LowPowerCoolingCapacity * LowPowerUnits
    + HighPowerCoolingCapacity * HighPowerUnits
    >= TotalCoolingRequired
)

model.addConstr(
    LowPowerElectricityUsage * LowPowerUnits
    + HighPowerElectricityUsage * HighPowerUnits
    <= TotalElectricityAvailable
)

model.addConstr(
    LowPowerUnits <= MaxLowPowerPercentage * (LowPowerUnits + HighPowerUnits)
)

model.addConstr(HighPowerUnits >= MinHighPowerModels)
model.addConstr(LowPowerUnits >= 0)
model.addConstr(HighPowerUnits >= 0)


# Define the objective
model.setObjective(LowPowerUnits + HighPowerUnits, GRB.MINIMIZE)


# Optimize the model
model.optimize()


# Output results safely
if model.Status == GRB.OPTIMAL:
    print("Optimal Objective Value: ", model.ObjVal)
    with open("output_solution.txt", "w") as f:
        f.write(str(model.ObjVal))
else:
    with open("output_solution.txt", "w") as f:
        f.write(str(model.Status))