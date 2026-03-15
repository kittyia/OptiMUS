
import os
import numpy as np
import json 
from gurobipy import Model, GRB, quicksum


model = Model("OptimizationProblem")

with open("data.json", "r") as f:
    data = json.load(f)




### Define the parameters

TotalMRNAAvailable = data["TotalMRNAAvailable"] # shape: [], definition: TotalMRNAAvailable

MRNAPerChildVaccine = data["MRNAPerChildVaccine"] # shape: [], definition: MRNAPerChildVaccine

MRNAPerAdultVaccine = data["MRNAPerAdultVaccine"] # shape: [], definition: Amount of mRNA required for each adult vaccine

FeverSuppressantPerChildVaccine = data["FeverSuppressantPerChildVaccine"] # shape: [], definition: FeverSuppressantPerChildVaccine

FeverSuppressantPerAdultVaccine = data["FeverSuppressantPerAdultVaccine"] # shape: [], definition: Amount of fever suppressant used in each adult vaccine

MinPercentageAdultVaccines = data["MinPercentageAdultVaccines"] # shape: [], definition: MinPercentageAdultVaccines

MinChildVaccines = data["MinChildVaccines"] # shape: [], definition: Minimum number of children's vaccines to be produced



### Define the variables

ChildVaccines = model.addVar(vtype=GRB.INTEGER, name="ChildVaccines")

AdultVaccines = model.addVar(vtype=GRB.INTEGER, name="AdultVaccines")



### Define the constraints

model.addConstr(MRNAPerChildVaccine * ChildVaccines + MRNAPerAdultVaccine * AdultVaccines <= TotalMRNAAvailable)
model.addConstr(
    (1 - MinPercentageAdultVaccines / 100.0) * AdultVaccines
    >= (MinPercentageAdultVaccines / 100.0) * ChildVaccines
)
model.addConstr(ChildVaccines >= MinChildVaccines])


### Define the objective

model.setObjective(
    FeverSuppressantPerChildVaccine * ChildVaccines +
    FeverSuppressantPerAdultVaccine * AdultVaccines,
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
