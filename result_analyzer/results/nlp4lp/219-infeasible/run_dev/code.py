
import os
import numpy as np
import json 
from gurobipy import Model, GRB, quicksum


model = Model("OptimizationProblem")

with open("data.json", "r") as f:
    data = json.load(f)




### Define the parameters

LowPowerCoolingCapacity = data["LowPowerCoolingCapacity"] # shape: [], definition: Cooling capacity of a low-powered air conditioner (number of housing units it can cool)

LowPowerElectricityUsage = data["LowPowerElectricityUsage"] # shape: [], definition: Electricity usage of a low-powered air conditioner (units per day)

HighPowerCoolingCapacity = data["HighPowerCoolingCapacity"] # shape: [], definition: Cooling capacity of a high-powered air conditioner (number of housing units it can cool)

HighPowerElectricityUsage = data["HighPowerElectricityUsage"] # shape: [], definition: Electricity usage of a high-powered air conditioner (units per day)

MaxLowPowerPercentage = data["MaxLowPowerPercentage"] # shape: [], definition: Maximum percentage of low-powered air conditioners allowed

MinHighPowerModels = data["MinHighPowerModels"] # shape: [], definition: Minimum number of high-powered air conditioners required

TotalCoolingRequired = data["TotalCoolingRequired"] # shape: [], definition: Total number of housing units to be cooled

TotalElectricityAvailable = data["TotalElectricityAvailable"] # shape: [], definition: Total units of electricity available



### Define the variables

LowPowerUnits = model.addVar(vtype=GRB.INTEGER, name="LowPowerUnits")

HighPowerUnits = model.addVar(vtype=GRB.INTEGER, name="HighPowerUnits")



### Define the constraints

model.addConstr(
    LowPowerCoolingCapacity * LowPowerUnits
    + HighPowerCoolingCapacity * HighPowerUnits
    >= TotalCoolingRequired
)
model.addConstr(
    LowPowerElectricityUsage * LowPowerUnits +
    HighPowerElectricityUsage * HighPowerUnits
    <= TotalElectricityAvailable
)
model.addConstr(LowPowerUnits <= MaxLowPowerPercentage * (LowPowerUnits + HighPowerUnits))
model.addConstr(HighPowerUnits >= MinHighPowerModels)
model.addConstr(LowPowerUnits >= 0)
model.addConstr(LowPowerUnits >= 0)
model.addConstr(HighPowerUnits >= 0)


### Define the objective

model.setObjective(LowPowerUnits + HighPowerUnits, GRB.MINIMIZE)


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
