
import os
import numpy as np
import json 
from gurobipy import Model, GRB, quicksum


model = Model("OptimizationProblem")

with open("data.json", "r") as f:
    data = json.load(f)




### Define the parameters

T = data["T"] # shape: [], definition: Number of time periods

Demand = data["Demand"] # shape: ['T'], definition: Demand for electricity in each time period

OilCap = data["OilCap"] # shape: ['T'], definition: Available capacity from existing oil-fired plants in each time period

CoalCost = data["CoalCost"] # shape: [], definition: Cost per unit of capacity for building a coal plant

NukeCost = data["NukeCost"] # shape: [], definition: Cost per unit of capacity for building a nuclear plant

MaxNuke = data["MaxNuke"] # shape: [], definition: Maximum fraction of total capacity that can be nuclear

CoalLife = data["CoalLife"] # shape: [], definition: Lifespan of a coal plant in time periods

NukeLife = data["NukeLife"] # shape: [], definition: Lifespan of a nuclear plant in time periods



### Define the variables

CoalBuild = model.addVars(T, vtype=GRB.CONTINUOUS, name="CoalBuild")

NukeBuild = model.addVars(T, vtype=GRB.CONTINUOUS, name="NukeBuild")

CoalCap = model.addVars(T, vtype=GRB.CONTINUOUS, name="CoalCap")

NukeCap = model.addVars(T, vtype=GRB.CONTINUOUS, name="NukeCap")



### Define the constraints

for t in range(T):
    coal_active = sum(CoalBuild[tau] 
                      for tau in range(max(0, t - CoalLife + 1), t + 1))
    nuke_active = sum(NukeBuild[tau] 
                      for tau in range(max(0, t - NukeLife + 1), t + 1))
    
    model.addConstr(
        OilCap[t] + coal_active + nuke_active >= Demand[t]
    )
for t in range(T):
    lower_bound = max(0, t - CoalLife + 1)
    model.addConstr(
        CoalCap[t] == sum(CoalBuild[k] for k in range(lower_bound, t + 1))
    )
for t in range(T):
    start_period = max(0, t - NukeLife + 1)
    model.addConstr(
        NukeCap[t] == sum(NukeBuild[tau] for tau in range(start_period, t + 1))
    )
for t in range(T):
    model.addConstr(
        NukeCap[t] <= MaxNuke * (OilCap[t] + CoalCap[t] + NukeCap[t])
    )
for t in range(T):
    model.addConstr(CoalBuild[t] >= 0)
    model.addConstr(NukeBuild[t] >= 0)


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
