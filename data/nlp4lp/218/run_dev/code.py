
import os
import numpy as np
import json 
from gurobipy import Model, GRB, quicksum


model = Model("OptimizationProblem")

with open("data.json", "r") as f:
    data = json.load(f)




### Define the parameters

GuestsPerMinuteDenselySeatedLift = data["GuestsPerMinuteDenselySeatedLift"] # shape: [], definition: Number of guests transported per minute by a densely-seated ski lift

GuestsPerMinuteLooselySeatedLift = data["GuestsPerMinuteLooselySeatedLift"] # shape: [], definition: Number of guests transported per minute by a loosely-seated ski lift

ElectricityPerDenselySeatedLift = data["ElectricityPerDenselySeatedLift"] # shape: [], definition: Electricity units used by a densely-seated ski lift

ElectricityPerLooselySeatedLift = data["ElectricityPerLooselySeatedLift"] # shape: [], definition: Electricity units used by a loosely-seated ski lift

MinimumLooselySeatedLifts = data["MinimumLooselySeatedLifts"] # shape: [], definition: Minimum number of loosely-seated ski lifts required

MinimumGuestsPerMinute = data["MinimumGuestsPerMinute"] # shape: [], definition: Minimum number of guests per minute required for profit

TotalElectricityAvailable = data["TotalElectricityAvailable"] # shape: [], definition: Total electricity units available



### Define the variables

DenselySeatedLifts = model.addVar(vtype=GRB.INTEGER, name="DenselySeatedLifts")

LooselySeatedLifts = model.addVar(vtype=GRB.INTEGER, name="LooselySeatedLifts")



### Define the constraints

model.addConstr(
    GuestsPerMinuteDenselySeatedLift * DenselySeatedLifts
    + GuestsPerMinuteLooselySeatedLift * LooselySeatedLifts
    >= MinimumGuestsPerMinute
)
model.addConstr(
    ElectricityPerDenselySeatedLift * DenselySeatedLifts
    + ElectricityPerLooselySeatedLift * LooselySeatedLifts
    <= TotalElectricityAvailable
)
model.addConstr(DenselySeatedLifts >= 0)
model.addConstr(LooselySeatedLifts >= MinimumLooselySeatedLifts)


### Define the objective

model.setObjective(DenselySeatedLifts + LooselySeatedLifts, GRB.MINIMIZE)


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
