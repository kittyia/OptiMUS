import os
import numpy as np
import json 
from gurobipy import Model, GRB, quicksum


model = Model("OptimizationProblem")

with open("data.json", "r") as f:
    data = json.load(f)


### Define the parameters

HeatingCapacityNew = data["HeatingCapacityNew"]
EnergyConsumptionNew = data["EnergyConsumptionNew"]
HeatingCapacityOld = data["HeatingCapacityOld"]
EnergyConsumptionOld = data["EnergyConsumptionOld"]
MaxFractionOld = data["MaxFractionOld"]
MinNewFurnaces = data["MinNewFurnaces"]
MinHeatingRequirement = data["MinHeatingRequirement"]
AvailableEnergy = data["AvailableEnergy"]


### Define the variables

NewFurnaces = model.addVar(vtype=GRB.INTEGER, name="NewFurnaces")
OldFurnaces = model.addVar(vtype=GRB.INTEGER, name="OldFurnaces")


### Define the constraints

model.addConstr(
    HeatingCapacityNew * NewFurnaces + 
    HeatingCapacityOld * OldFurnaces 
    >= MinHeatingRequirement
)

model.addConstr(
    EnergyConsumptionNew * NewFurnaces + 
    EnergyConsumptionOld * OldFurnaces 
    <= AvailableEnergy
)

model.addConstr(
    OldFurnaces <= MaxFractionOld * (NewFurnaces + OldFurnaces)
)

model.addConstr(NewFurnaces >= MinNewFurnaces)
model.addConstr(OldFurnaces >= 0)


### Define the objective

model.setObjective(NewFurnaces + OldFurnaces, GRB.MINIMIZE)


### Optimize the model

model.optimize()


### Output results safely

if model.status == GRB.OPTIMAL:
    print("Optimal Objective Value:", model.ObjVal)
    with open("output_solution.txt", "w") as f:
        f.write(str(model.ObjVal))
else:
    print("Optimization was not successful. Status code:", model.status)
    with open("output_solution.txt", "w") as f:
        f.write(str(model.status))