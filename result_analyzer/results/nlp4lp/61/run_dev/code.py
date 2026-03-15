
import os
import numpy as np
import json 
from gurobipy import Model, GRB, quicksum


model = Model("OptimizationProblem")

with open("data.json", "r") as f:
    data = json.load(f)




### Define the parameters

WashRateTopLoading = data["WashRateTopLoading"] # shape: [], definition: Number of items washed per day by a top-loading machine

WashRateFrontLoading = data["WashRateFrontLoading"] # shape: [], definition: Number of items washed per day by a front-loading machine

EnergyConsumptionTopLoading = data["EnergyConsumptionTopLoading"] # shape: [], definition: Energy consumed per day by a top-loading machine (kWh)

EnergyConsumptionFrontLoading = data["EnergyConsumptionFrontLoading"] # shape: [], definition: Energy consumed per day by a front-loading machine (kWh)

MinItemsPerDay = data["MinItemsPerDay"] # shape: [], definition: Minimum number of items to wash per day

MaxEnergyPerDay = data["MaxEnergyPerDay"] # shape: [], definition: Maximum available energy per day (kWh)

MaxFractionTopLoading = data["MaxFractionTopLoading"] # shape: [], definition: Maximum fraction of machines that can be top-loading

MinNumFrontLoading = data["MinNumFrontLoading"] # shape: [], definition: Minimum number of front-loading machines



### Define the variables

TopLoadingMachines = model.addVar(vtype=GRB.INTEGER, name="TopLoadingMachines")

FrontLoadingMachines = model.addVar(vtype=GRB.INTEGER, name="FrontLoadingMachines")



### Define the constraints

model.addConstr(
    WashRateTopLoading * TopLoadingMachines +
    WashRateFrontLoading * FrontLoadingMachines
    >= MinItemsPerDay
)
model.addConstr(
    EnergyConsumptionTopLoading * TopLoadingMachines
    + EnergyConsumptionFrontLoading * FrontLoadingMachines
    <= MaxEnergyPerDay
)
model.addConstr(
    TopLoadingMachines <= MaxFractionTopLoading * (TopLoadingMachines + FrontLoadingMachines)
)
model.addConstr(FrontLoadingMachines >= MinNumFrontLoading)
model.addConstr(TopLoadingMachines >= 0)
model.addConstr(TopLoadingMachines >= 0)
model.addConstr(FrontLoadingMachines >= 0)


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
