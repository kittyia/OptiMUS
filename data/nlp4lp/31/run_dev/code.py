
import os
import numpy as np
import json 
from gurobipy import Model, GRB, quicksum


model = Model("OptimizationProblem")

with open("data.json", "r") as f:
    data = json.load(f)




### Define the parameters

MinimumDemandHardwood = data["MinimumDemandHardwood"] # shape: [], definition: Minimum expected weekly demand for hardwood

MinimumDemandVinyl = data["MinimumDemandVinyl"] # shape: [], definition: Minimum expected weekly demand for vinyl planks

MinimumTotalShipping = data["MinimumTotalShipping"] # shape: [], definition: Minimum total square feet of flooring to be shipped weekly

MaxProductionHardwood = data["MaxProductionHardwood"] # shape: [], definition: Maximum weekly production capacity for hardwood

MaxProductionVinyl = data["MaxProductionVinyl"] # shape: [], definition: Maximum weekly production capacity for vinyl planks

ProfitHardwood = data["ProfitHardwood"] # shape: [], definition: Profit per square foot of hardwood

ProfitVinyl = data["ProfitVinyl"] # shape: [], definition: Profit per square foot of vinyl planks



### Define the variables

HardwoodProduction = model.addVar(vtype=GRB.CONTINUOUS, name="HardwoodProduction")

VinylProduction = model.addVar(vtype=GRB.CONTINUOUS, name="VinylProduction")



### Define the constraints

model.addConstr(HardwoodProduction >= MinimumDemandHardwood)
model.addConstr(VinylProduction >= MinimumDemandVinyl)
model.addConstr(HardwoodProduction + VinylProduction >= MinimumTotalShipping)
model.addConstr(HardwoodProduction <= MaxProductionHardwood)
model.addConstr(VinylProduction <= MaxProductionVinyl)


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
