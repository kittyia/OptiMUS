
import os
import numpy as np
import json 
from gurobipy import Model, GRB, quicksum


model = Model("OptimizationProblem")

with open("data.json", "r") as f:
    data = json.load(f)




### Define the parameters

PackagesDeliveredRegular = data["PackagesDeliveredRegular"] # shape: [], definition: Number of packages a regular van can deliver per day

PackagesDeliveredHybrid = data["PackagesDeliveredHybrid"] # shape: [], definition: Number of packages a hybrid van can deliver per day

PollutantsRegular = data["PollutantsRegular"] # shape: [], definition: Number of pollutant units produced by a regular van per day

PollutantsHybrid = data["PollutantsHybrid"] # shape: [], definition: Number of pollutant units produced by a hybrid van per day

MaxPollutants = data["MaxPollutants"] # shape: [], definition: Maximum allowed pollutant units per day

MinPackages = data["MinPackages"] # shape: [], definition: Minimum required number of packages per day



### Define the variables

RegularVans = model.addVar(vtype=GRB.INTEGER, name="RegularVans")

HybridVans = model.addVar(vtype=GRB.INTEGER, name="HybridVans")



### Define the constraints

model.addConstr(PollutantsRegular * RegularVans + PollutantsHybrid * HybridVans <= MaxPollutants)
model.addConstr(PackagesDeliveredRegular * RegularVans + PackagesDeliveredHybrid * HybridVans >= MinPackages)
model.addConstr(RegularVans >= 0)
model.addConstr(HybridVans >= 0)


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
