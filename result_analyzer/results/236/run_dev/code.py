
import os
import numpy as np
import json 
from gurobipy import Model, GRB, quicksum


model = Model("OptimizationProblem")

with open("data.json", "r") as f:
    data = json.load(f)




### Define the parameters

NumTypes = data["NumTypes"] # shape: [], definition: Number of types of lights available

ElectricityUsage = data["ElectricityUsage"] # shape: ['NumTypes'], definition: Electricity units used per hour by each type of light

ChangesPerDecade = data["ChangesPerDecade"] # shape: ['NumTypes'], definition: Number of times each type of light needs to be changed per decade

MinPercentageFluorescence = data["MinPercentageFluorescence"] # shape: [], definition: Minimum fraction of implemented light fixtures that must be fluorescence lamps

MinNumFixtures = data["MinNumFixtures"] # shape: [], definition: Minimum number of light fixtures required

MaxElectricity = data["MaxElectricity"] # shape: [], definition: Maximum number of electricity units that can be used



### Define the variables

NumLights = model.addVars(NumTypes, vtype=GRB.INTEGER, name="NumLights")



### Define the constraints

model.addConstr(sum(NumLights[t] for t in range(NumTypes)) >= MinNumFixtures)
model.addConstr(
    sum(ElectricityUsage[i] * NumLights[i] for i in range(NumTypes)) <= MaxElectricity
)
model.addConstr(
    NumLights[1] >= MinPercentageFluorescence * sum(NumLights[t] for t in range(NumTypes))
)
for t in range(NumTypes):
    model.addConstr(NumLights[t] >= 0)


### Define the objective

model.setObjective(quicksum(ChangesPerDecade[i] * NumLights[i] for i in range(NumTypes)), GRB.MINIMIZE)


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
