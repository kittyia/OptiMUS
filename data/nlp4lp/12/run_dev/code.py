
import os
import numpy as np
import json 
from gurobipy import Model, GRB, quicksum


model = Model("OptimizationProblem")

with open("data.json", "r") as f:
    data = json.load(f)




### Define the parameters

MaxHeatingTime = data["MaxHeatingTime"] # shape: [], definition: Maximum available time for the heating machine per day

MaxCoolingTime = data["MaxCoolingTime"] # shape: [], definition: Maximum available time for the cooling machine per day

HeatingRegular = data["HeatingRegular"] # shape: [], definition: Heating time required to produce one regular glass pane

CoolingRegular = data["CoolingRegular"] # shape: [], definition: Cooling time required to produce one regular glass pane

HeatingTempered = data["HeatingTempered"] # shape: [], definition: Heating time required to produce one tempered glass pane

CoolingTempered = data["CoolingTempered"] # shape: [], definition: Cooling time required to produce one tempered glass pane

ProfitRegular = data["ProfitRegular"] # shape: [], definition: Profit per regular glass pane

ProfitTempered = data["ProfitTempered"] # shape: [], definition: Profit per tempered glass pane



### Define the variables

RegularPanes = model.addVar(vtype=GRB.INTEGER, name="RegularPanes")

TemperedPanes = model.addVar(vtype=GRB.INTEGER, name="TemperedPanes")



### Define the constraints

model.addConstr(HeatingRegular * RegularPanes + HeatingTempered * TemperedPanes <= MaxHeatingTime)
model.addConstr(CoolingRegular * RegularPanes + CoolingTempered * TemperedPanes <= MaxCoolingTime)
model.addConstr(RegularPanes >= 0)
model.addConstr(TemperedPanes >= 0)


### Define the objective

model.setObjective(ProfitRegular * RegularPanes + ProfitTempered * TemperedPanes, GRB.MAXIMIZE)


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
