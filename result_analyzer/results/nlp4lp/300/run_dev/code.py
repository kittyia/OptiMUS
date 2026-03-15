
import os
import numpy as np
import json 
from gurobipy import Model, GRB, quicksum


model = Model("OptimizationProblem")

with open("data.json", "r") as f:
    data = json.load(f)




### Define the parameters

NumPatients = data["NumPatients"] # shape: [], definition: Number of patients to be transported daily

CapacityAmbulance = data["CapacityAmbulance"] # shape: [], definition: Capacity of a Type II ambulance in terms of patients per shift

CostAmbulance = data["CostAmbulance"] # shape: [], definition: Cost of a Type II ambulance per shift

CapacityVan = data["CapacityVan"] # shape: [], definition: Capacity of a hospital van in terms of patients per shift

CostVan = data["CostVan"] # shape: [], definition: Cost of a hospital van per shift

MaxVanShiftsPercent = data["MaxVanShiftsPercent"] # shape: [], definition: Maximum percentage of shifts that can be hospital vans



### Define the variables

AmbulanceShifts = model.addVar(vtype=GRB.INTEGER, name="AmbulanceShifts")

VanShifts = model.addVar(vtype=GRB.INTEGER, name="VanShifts")



### Define the constraints

model.addConstr(CapacityAmbulance * AmbulanceShifts + CapacityVan * VanShifts >= NumPatients)
model.addConstr(VanShifts <= MaxVanShiftsPercent * (AmbulanceShifts + VanShifts))
model.addConstr(AmbulanceShifts >= 0)
model.addConstr(VanShifts >= 0)


### Define the objective

model.setObjective(CostAmbulance * AmbulanceShifts + CostVan * VanShifts, GRB.MINIMIZE)


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
