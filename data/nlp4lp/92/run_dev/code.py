
import os
import numpy as np
import json 
from gurobipy import Model, GRB, quicksum


model = Model("OptimizationProblem")

with open("data.json", "r") as f:
    data = json.load(f)




### Define the parameters

NumBeakers = data["NumBeakers"] # shape: [], definition: Number of beakers

FlourAvailable = data["FlourAvailable"] # shape: [], definition: Amount of flour available

SpecialLiquidAvailable = data["SpecialLiquidAvailable"] # shape: [], definition: Amount of special liquid available

MaxWasteAllowed = data["MaxWasteAllowed"] # shape: [], definition: Maximum amount of waste allowed

FlourUsagePerBeaker = data["FlourUsagePerBeaker"] # shape: ['NumBeakers'], definition: Amount of flour used by each beaker

SpecialLiquidUsagePerBeaker = data["SpecialLiquidUsagePerBeaker"] # shape: ['NumBeakers'], definition: Amount of special liquid used by each beaker

SlimeProducedPerBeaker = data["SlimeProducedPerBeaker"] # shape: ['NumBeakers'], definition: Amount of slime produced by each beaker

WasteProducedPerBeaker = data["WasteProducedPerBeaker"] # shape: ['NumBeakers'], definition: Amount of waste produced by each beaker



### Define the variables

BeakersUsed = model.addVars(NumBeakers, vtype=GRB.INTEGER, name="BeakersUsed")



### Define the constraints

model.addConstr(
    sum(FlourUsagePerBeaker[i] * BeakersUsed[i] for i in range(NumBeakers)) 
    <= FlourAvailable
)
model.addConstr(
    sum(SpecialLiquidUsagePerBeaker[i] * BeakersUsed[i] for i in range(NumBeakers))
    <= SpecialLiquidAvailable
)
model.addConstr(
    sum(WasteProducedPerBeaker[i] * BeakersUsed[i] for i in range(NumBeakers)) 
    <= MaxWasteAllowed
)
for i in range(NumBeakers):
    model.addConstr(BeakersUsed[i] >= 0)


### Define the objective

model.setObjective(quicksum(SlimeProducedPerBeaker[i] * BeakersUsed[i] for i in range(NumBeakers)), GRB.MAXIMIZE)


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
