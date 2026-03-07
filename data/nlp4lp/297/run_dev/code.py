
import os
import numpy as np
import json 
from gurobipy import Model, GRB, quicksum


model = Model("OptimizationProblem")

with open("data.json", "r") as f:
    data = json.load(f)




### Define the parameters

TotalArea = data["TotalArea"] # shape: [], definition: Total area of grass land in square feet

TimeHeavyDuty = data["TimeHeavyDuty"] # shape: [], definition: Time required in seconds to cut one square foot of land using the heavy-duty yard machine

TimeGasMower = data["TimeGasMower"] # shape: [], definition: Time required in seconds to cut one square foot of land using the gas lawn mower

PollutionHeavyDuty = data["PollutionHeavyDuty"] # shape: [], definition: Pollution produced per square foot by the heavy-duty yard machine

PollutionGasMower = data["PollutionGasMower"] # shape: [], definition: Pollution produced per square foot by the gas lawn mower

FuelHeavyDuty = data["FuelHeavyDuty"] # shape: [], definition: Fuel required per square foot by the heavy-duty yard machine

FuelGasMower = data["FuelGasMower"] # shape: [], definition: Fuel required per square foot by the gas lawn mower

TotalFuel = data["TotalFuel"] # shape: [], definition: Total units of fuel available

MaxPollution = data["MaxPollution"] # shape: [], definition: Maximum allowable units of pollution



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

print("Optimal Objective Value: ", model.objVal)


if model.status == GRB.OPTIMAL:
    with open("output_solution.txt", "w") as f:
        f.write(str(model.objVal))
    print("Optimal Objective Value: ", model.objVal)
else:
    with open("output_solution.txt", "w") as f:
        f.write(model.status)
