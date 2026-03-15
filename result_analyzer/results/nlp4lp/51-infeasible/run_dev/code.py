
import os
import numpy as np
import json 
from gurobipy import Model, GRB, quicksum


model = Model("OptimizationProblem")

with open("data.json", "r") as f:
    data = json.load(f)




### Define the parameters

HeatingCapacityNew = data["HeatingCapacityNew"] # shape: [], definition: HeatingCapacityNew

EnergyConsumptionNew = data["EnergyConsumptionNew"] # shape: [], definition: EnergyConsumptionNew

HeatingCapacityOld = data["HeatingCapacityOld"] # shape: [], definition: HeatingCapacityOld

EnergyConsumptionOld = data["EnergyConsumptionOld"] # shape: [], definition: EnergyConsumptionOld

MaxFractionOld = data["MaxFractionOld"] # shape: [], definition: MaxFractionOld

MinNewFurnaces = data["MinNewFurnaces"] # shape: [], definition: MinNewFurnaces

MinHeatingRequirement = data["MinHeatingRequirement"] # shape: [], definition: MinHeatingRequirement

AvailableEnergy = data["AvailableEnergy"] # shape: [], definition: AvailableEnergy



### Define the variables

NewFurnaces = model.addVar(vtype=GRB.INTEGER, name="NewFurnaces")

OldFurnaces = model.addVar(vtype=GRB.INTEGER, name="OldFurnaces")



### Define the constraints

model.addConstr(HeatingCapacityNew * NewFurnaces + HeatingCapacityOld * OldFurnaces >= MinHeatingRequirement)
model.addConstr(EnergyConsumptionNew * NewFurnaces + EnergyConsumptionOld * OldFurnaces <= AvailableEnergy)
model.addConstr(OldFurnaces <= MaxFractionOld * (NewFurnaces + OldFurnaces))
model.addConstr(NewFurnaces >= MinNewFurnaces)
model.addConstr(OldFurnaces >= 0)


### Define the objective

model.setObjective(NewFurnaces + OldFurnaces, GRB.MINIMIZE)


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
