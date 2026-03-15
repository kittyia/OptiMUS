import os
import numpy as np
import json
from gurobipy import Model, GRB, quicksum


model = Model("OptimizationProblem")

with open("data.json", "r") as f:
    data = json.load(f)


# Define the parameters
MedicinalIngredientPerRegularBatch = data["MedicinalIngredientPerRegularBatch"]
RehydrationProductPerRegularBatch = data["RehydrationProductPerRegularBatch"]
MedicinalIngredientPerPremiumBatch = data["MedicinalIngredientPerPremiumBatch"]
RehydrationProductPerPremiumBatch = data["RehydrationProductPerPremiumBatch"]
TotalMedicinalIngredients = data["TotalMedicinalIngredients"]
TotalRehydrationProduct = data["TotalRehydrationProduct"]
MinRegularBatches = data["MinRegularBatches"]
PeopleTreatedPerRegularBatch = data["PeopleTreatedPerRegularBatch"]
PeopleTreatedPerPremiumBatch = data["PeopleTreatedPerPremiumBatch"]


# Define the variables
RegularBatches = model.addVar(vtype=GRB.INTEGER, name="RegularBatches")
PremiumBatches = model.addVar(vtype=GRB.INTEGER, name="PremiumBatches")


# Define the constraints
model.addConstr(
    MedicinalIngredientPerRegularBatch * RegularBatches
    + MedicinalIngredientPerPremiumBatch * PremiumBatches
    <= TotalMedicinalIngredients
)

model.addConstr(
    RehydrationProductPerRegularBatch * RegularBatches
    + RehydrationProductPerPremiumBatch * PremiumBatches
    <= TotalRehydrationProduct
)

model.addConstr(RegularBatches <= PremiumBatches - 1)
model.addConstr(RegularBatches >= MinRegularBatches)


# Define the objective
model.setObjective(
    PeopleTreatedPerRegularBatch * RegularBatches
    + PeopleTreatedPerPremiumBatch * PremiumBatches,
    GRB.MAXIMIZE
)


# Optimize the model
model.optimize()


# Output optimal objective value
if model.status == GRB.OPTIMAL:
    print("Optimal Objective Value: ", model.objVal)
    with open("output_solution.txt", "w") as f:
        f.write(str(model.objVal))
else:
    with open("output_solution.txt", "w") as f:
        f.write(str(model.status))