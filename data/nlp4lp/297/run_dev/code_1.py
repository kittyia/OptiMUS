import os
import numpy as np
import json 
from gurobipy import Model, GRB, quicksum


model = Model("OptimizationProblem")

with open("data.json", "r") as f:
    data = json.load(f)


### Define the parameters

TotalArea = data["TotalArea"]

TimeHeavyDuty = data["TimeHeavyDuty"]

TimeGasMower = data["TimeGasMower"]

PollutionHeavyDuty = data["PollutionHeavyDuty"]

PollutionGasMower = data["PollutionGasMower"]

FuelHeavyDuty = data["FuelHeavyDuty"]

FuelGasMower = data["FuelGasMower"]

TotalFuel = data["TotalFuel"]

MaxPollution = data["MaxPollution"]


### Define the variables

HeavyArea = model.addVar(vtype=GRB.CONTINUOUS, name="HeavyArea")

GasArea = model.addVar(vtype=GRB.CONTINUOUS, name="GasArea")


### Define the constraints

model.addConstr(HeavyArea + GasArea == TotalArea)
model.addConstr(FuelHeavyDuty * HeavyArea + FuelGasMower * GasArea <= TotalFuel)
model.addConstr(PollutionHeavyDuty * HeavyArea + PollutionGasMower * GasArea <= MaxPollution)
model.addConstr(HeavyArea >= 0)
model.addConstr(GasArea >= 0)


### Define the objective

model.setObjective(TimeHeavyDuty * HeavyArea + TimeGasMower * GasArea, GRB.MINIMIZE)


### Optimize the model

model.optimize()


### Output optimal objective value

if model.status == GRB.OPTIMAL:
    print("Optimal Objective Value: ", model.ObjVal)
    with open("output_solution.txt", "w") as f:
        f.write(str(model.ObjVal))
else:
    with open("output_solution.txt", "w") as f:
        f.write(str(model.status))
``