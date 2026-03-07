
import os
import numpy as np
import json 
from gurobipy import Model, GRB, quicksum


model = Model("OptimizationProblem")

with open("data.json", "r") as f:
    data = json.load(f)




### Define the parameters

ImportedMaterialPerDoseA = data["ImportedMaterialPerDoseA"] # shape: [], definition: Amount of imported material required to produce one dose of medicine A

MRNAPerDoseA = data["MRNAPerDoseA"] # shape: [], definition: Amount of mRNA required to produce one dose of medicine A

ImportedMaterialPerDoseB = data["ImportedMaterialPerDoseB"] # shape: [], definition: Amount of imported material required to produce one dose of medicine B

MRNAPerDoseB = data["MRNAPerDoseB"] # shape: [], definition: Amount of mRNA required to produce one dose of medicine B

MaxImportedMaterial = data["MaxImportedMaterial"] # shape: [], definition: Maximum available units of imported material

MaxMRNA = data["MaxMRNA"] # shape: [], definition: Maximum available units of mRNA

MaxDosesA = data["MaxDosesA"] # shape: [], definition: Maximum number of doses of medicine A that can be produced

TreatmentPerDoseA = data["TreatmentPerDoseA"] # shape: [], definition: Number of people treated by one dose of medicine A

TreatmentPerDoseB = data["TreatmentPerDoseB"] # shape: [], definition: Number of people treated by one dose of medicine B



### Define the variables

DosesA = model.addVar(vtype=GRB.INTEGER, name="DosesA")

DosesB = model.addVar(vtype=GRB.INTEGER, name="DosesB")



### Define the constraints

model.addConstr(ImportedMaterialPerDoseA * DosesA + ImportedMaterialPerDoseB * DosesB <= MaxImportedMaterial)
model.addConstr(MRNAPerDoseA * DosesA + MRNAPerDoseB * DosesB <= MaxMRNA)
model.addConstr(DosesA <= MaxDosesA)
model.addConstr(DosesB >= DosesA + 1)
model.addConstr(DosesA >= 0)
model.addConstr(DosesB >= 0)


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
