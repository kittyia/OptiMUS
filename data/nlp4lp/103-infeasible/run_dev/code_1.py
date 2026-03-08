import os
import numpy as np
import json
from gurobipy import Model, GRB, quicksum


model = Model("OptimizationProblem")

with open("data.json", "r") as f:
    data = json.load(f)


### Define the parameters

TotalMRNAAvailable = data["TotalMRNAAvailable"]

MRNAPerChildVaccine = data["MRNAPerChildVaccine"]

MRNAPerAdultVaccine = data["MRNAPerAdultVaccine"]

FeverSuppressantPerChildVaccine = data["FeverSuppressantPerChildVaccine"]

FeverSuppressantPerAdultVaccine = data["FeverSuppressantPerAdultVaccine"]

MinPercentageAdultVaccines = data["MinPercentageAdultVaccines"]

MinChildVaccines = data["MinChildVaccines"]


### Define the variables

ChildVaccines = model.addVar(vtype=GRB.INTEGER, name="ChildVaccines")

AdultVaccines = model.addVar(vtype=GRB.INTEGER, name="AdultVaccines")


### Define the constraints

# mRNA availability constraint
model.addConstr(
    MRNAPerChildVaccine * ChildVaccines +
    MRNAPerAdultVaccine * AdultVaccines
    <= TotalMRNAAvailable
)

# At least MinPercentageAdultVaccines% of total vaccines are adult vaccines
model.addConstr(
    (1 - MinPercentageAdultVaccines / 100.0) * AdultVaccines
    >= (MinPercentageAdultVaccines / 100.0) * ChildVaccines
)

# Minimum number of children's vaccines
model.addConstr(ChildVaccines >= MinChildVaccines)


### Define the objective

model.setObjective(
    FeverSuppressantPerChildVaccine * ChildVaccines +
    FeverSuppressantPerAdultVaccine * AdultVaccines,
    GRB.MINIMIZE
)


### Optimize the model

model.optimize()


### Output optimal objective value

if model.status == GRB.OPTIMAL:
    print("Optimal Objective Value: ", model.objVal)
    with open("output_solution.txt", "w") as f:
        f.write(str(model.objVal))
else:
    with open("output_solution.txt", "w") as f:
        f.write(str(model.status))