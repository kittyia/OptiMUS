
import os
import numpy as np
import json 
from gurobipy import Model, GRB, quicksum


model = Model("OptimizationProblem")

with open("data.json", "r") as f:
    data = json.load(f)




### Define the parameters

PrepTimeInVivo = data["PrepTimeInVivo"] # shape: [], definition: Preparation time required for in-vivo experiments

ExecTimeInVivo = data["ExecTimeInVivo"] # shape: [], definition: Execution time required for in-vivo experiments

RadiationInVivo = data["RadiationInVivo"] # shape: [], definition: Radiation units received from in-vivo experiments

PrepTimeExVivo = data["PrepTimeExVivo"] # shape: [], definition: Preparation time required for ex-vivo experiments

ExecTimeExVivo = data["ExecTimeExVivo"] # shape: [], definition: Execution time required for ex-vivo experiments

RadiationExVivo = data["RadiationExVivo"] # shape: [], definition: Radiation units received from ex-vivo experiments

MaxPrepTime = data["MaxPrepTime"] # shape: [], definition: Maximum available preparation time

MaxExecTime = data["MaxExecTime"] # shape: [], definition: Maximum available execution time



### Define the variables

InVivoExperiments = model.addVar(vtype=GRB.INTEGER, name="InVivoExperiments")

ExVivoExperiments = model.addVar(vtype=GRB.INTEGER, name="ExVivoExperiments")



### Define the constraints

model.addConstr(PrepTimeInVivo * InVivoExperiments + PrepTimeExVivo * ExVivoExperiments <= MaxPrepTime)
model.addConstr(ExecTimeInVivo * InVivoExperiments + ExecTimeExVivo * ExVivoExperiments <= MaxExecTime)
model.addConstr(InVivoExperiments >= 0)
model.addConstr(ExVivoExperiments >= 0)


### Define the objective

model.setObjective(
    RadiationInVivo * InVivoExperiments + RadiationExVivo * ExVivoExperiments,
    GRB.MINIMIZE
)


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
