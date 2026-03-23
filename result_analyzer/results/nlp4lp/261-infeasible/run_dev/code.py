
import os
import numpy as np
import json 
from gurobipy import Model, GRB, quicksum


model = Model("OptimizationProblem")

with open("data.json", "r") as f:
    data = json.load(f)




### Define the parameters

NorthernFactoryAntiItchRate = data["NorthernFactoryAntiItchRate"] # shape: [], definition: Production rate of anti-itch injections per hour at the northern factory

NorthernFactoryTopicalCreamRate = data["NorthernFactoryTopicalCreamRate"] # shape: [], definition: Production rate of topical cream per hour at the northern factory

WesternFactoryAntiItchRate = data["WesternFactoryAntiItchRate"] # shape: [], definition: Production rate of anti-itch injections per hour at the western factory

WesternFactoryTopicalCreamRate = data["WesternFactoryTopicalCreamRate"] # shape: [], definition: Production rate of topical cream per hour at the western factory

NorthernFactoryPlasticUsage = data["NorthernFactoryPlasticUsage"] # shape: [], definition: Units of plastic required per hour at the northern factory

WesternFactoryPlasticUsage = data["WesternFactoryPlasticUsage"] # shape: [], definition: Units of plastic required per hour at the western factory

TotalPlasticAvailable = data["TotalPlasticAvailable"] # shape: [], definition: Total units of plastic available

MinimumAntiItchProduction = data["MinimumAntiItchProduction"] # shape: [], definition: Minimum grams of anti-itch injections to produce

MinimumTopicalCreamProduction = data["MinimumTopicalCreamProduction"] # shape: [], definition: Minimum grams of topical cream to produce



### Define the variables

NorthernFactoryHours = model.addVar(vtype=GRB.CONTINUOUS, name="NorthernFactoryHours")

WesternFactoryHours = model.addVar(vtype=GRB.CONTINUOUS, name="WesternFactoryHours")



### Define the constraints

model.addConstr(
    NorthernFactoryAntiItchRate * NorthernFactoryHours +
    WesternFactoryAntiItchRate * WesternFactoryHours
    >= MinimumAntiItchProduction
)
model.addConstr(
    NorthernFactoryTopicalCreamRate * NorthernFactoryHours +
    WesternFactoryTopicalCreamRate * WesternFactoryHours
    >= MinimumTopicalCreamProduction
)
model.addConstr(
    NorthernFactoryPlasticUsage * NorthernFactoryHours
    + WesternFactoryPlasticUsage * WesternFactoryHours
    <= TotalPlasticAvailable
)
model.addConstr(NorthernFactoryHours >= 0)
model.addConstr(WesternFactoryHours >= 0)


### Define the objective

model.setObjective(NorthernFactoryHours + WesternFactoryHours, GRB.MINIMIZE)


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
