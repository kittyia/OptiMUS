
import os
import numpy as np
import json 
from gurobipy import Model, GRB, quicksum


model = Model("OptimizationProblem")

with open("data.json", "r") as f:
    data = json.load(f)




### Define the parameters

WaterSubsoil = data["WaterSubsoil"] # shape: [], definition: Amount of water required to hydrate one bag of subsoil per day

WaterTopsoil = data["WaterTopsoil"] # shape: [], definition: Amount of water required to hydrate one bag of topsoil per day

MaxTotalBags = data["MaxTotalBags"] # shape: [], definition: Maximum number of bags of topsoil and subsoil combined

MinTopsoilBags = data["MinTopsoilBags"] # shape: [], definition: Minimum number of topsoil bags to be used

MaxTopsoilProportion = data["MaxTopsoilProportion"] # shape: [], definition: Maximum proportion of bags that can be topsoil



### Define the variables

SubsoilBags = model.addVar(vtype=GRB.INTEGER, name="SubsoilBags")

TopsoilBags = model.addVar(vtype=GRB.INTEGER, name="TopsoilBags")



### Define the constraints

model.addConstr(SubsoilBags + TopsoilBags <= MaxTotalBags)
model.addConstr(TopsoilBags >= MinTopsoilBags)
model.addConstr(TopsoilBags <= MaxTopsoilProportion * (TopsoilBags + SubsoilBags))
model.addConstr(SubsoilBags >= 0)


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
