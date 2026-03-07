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

areaHeavyDuty = model.addVar(vtype=GRB.CONTINUOUS, name="areaHeavyDuty")
areaGasMower = model.addVar(vtype=GRB.CONTINUOUS, name="areaGasMower")


### Define the constraints

model.addConstr(areaHeavyDuty + areaGasMower == TotalArea)
model.addConstr(FuelHeavyDuty * areaHeavyDuty + FuelGasMower * areaGasMower <= TotalFuel)
model.addConstr(PollutionHeavyDuty * areaHeavyDuty + PollutionGasMower * areaGasMower <= MaxPollution)
model.addConstr(areaHeavyDuty >= 0)
model.addConstr(areaGasMower >= 0)


### Define the objective

model.setObjective(TimeHeavyDuty * areaHeavyDuty + TimeGasMower * areaGasMower, GRB.MINIMIZE)


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