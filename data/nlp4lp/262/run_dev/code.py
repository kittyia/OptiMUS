
import os
import numpy as np
import json 
from gurobipy import Model, GRB, quicksum


model = Model("OptimizationProblem")

with open("data.json", "r") as f:
    data = json.load(f)




### Define the parameters

PreparationTimeMedicationPatch = data["PreparationTimeMedicationPatch"] # shape: [], definition: Preparation time per batch of medication patches

PreparationTimeAntiBioticCream = data["PreparationTimeAntiBioticCream"] # shape: [], definition: Preparation time per batch of anti-biotic creams

MaterialRequiredMedicationPatch = data["MaterialRequiredMedicationPatch"] # shape: [], definition: Material required per batch of medication patches

MaterialRequiredAntiBioticCream = data["MaterialRequiredAntiBioticCream"] # shape: [], definition: Material required per batch of anti-biotic creams

MinRatioAntiBioticCreamToMedicationPatch = data["MinRatioAntiBioticCreamToMedicationPatch"] # shape: [], definition: Minimum ratio of anti-biotic creams to medication patches

MaxTotalBatches = data["MaxTotalBatches"] # shape: [], definition: Maximum total number of batches

AvailableStaffTime = data["AvailableStaffTime"] # shape: [], definition: Available staff time in minutes

AvailableMaterials = data["AvailableMaterials"] # shape: [], definition: Available units of materials

TreatmentPerBatchMedicationPatch = data["TreatmentPerBatchMedicationPatch"] # shape: [], definition: Number of people treated by each batch of medication patches

TreatmentPerBatchAntiBioticCream = data["TreatmentPerBatchAntiBioticCream"] # shape: [], definition: Number of people treated by each batch of anti-biotic creams



### Define the variables

MedicationPatches = model.addVar(vtype=GRB.INTEGER, name="MedicationPatches")

AntiBioticCreams = model.addVar(vtype=GRB.INTEGER, name="AntiBioticCreams")



### Define the constraints

model.addConstr(
    PreparationTimeMedicationPatch * MedicationPatches
    + PreparationTimeAntiBioticCream * AntiBioticCreams
    <= AvailableStaffTime
)
model.addConstr(MaterialRequiredMedicationPatch * MedicationPatches + MaterialRequiredAntiBioticCream * AntiBioticCreams <= AvailableMaterials)
model.addConstr(AntiBioticCreams >= MinRatioAntiBioticCreamToMedicationPatch * MedicationPatches)
model.addConstr(MedicationPatches >= 0)
model.addConstr(AntiBioticCreams >= 0)


### Define the objective

model.setObjective(
    TreatmentPerBatchMedicationPatch * MedicationPatches +
    TreatmentPerBatchAntiBioticCream * AntiBioticCreams,
    GRB.MAXIMIZE
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
