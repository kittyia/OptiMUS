
import os
import numpy as np
import json 
from gurobipy import Model, GRB, quicksum


model = Model("OptimizationProblem")

with open("data.json", "r") as f:
    data = json.load(f)




### Define the parameters

NumExperiments = data["NumExperiments"] # shape: [], definition: Number of experiments

NumResources = data["NumResources"] # shape: [], definition: Number of resource types

ResourceAvailable = data["ResourceAvailable"] # shape: ['NumResources'], definition: Amount of resource j available

ResourceRequired = data["ResourceRequired"] # shape: ['NumResources', 'NumExperiments'], definition: Amount of resource j required for experiment i

ElectricityProduced = data["ElectricityProduced"] # shape: ['NumExperiments'], definition: Amount of electricity produced by experiment i



### Define the variables

Experiments = model.addVars(NumExperiments, vtype=GRB.INTEGER, name="Experiments")



### Define the constraints

model.addConstr(3 * Experiments[0] + 5 * Experiments[1] <= 800)
model.addConstr(
    sum(ResourceRequired[1][i] * Experiments[i] for i in range(NumExperiments))
    <= ResourceAvailable[1]
)
for i in range(NumExperiments):
    model.addConstr(Experiments[i] >= 0)


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
