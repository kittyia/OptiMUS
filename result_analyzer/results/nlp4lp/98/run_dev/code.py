
import os
import numpy as np
import json 
from gurobipy import Model, GRB, quicksum


model = Model("OptimizationProblem")

with open("data.json", "r") as f:
    data = json.load(f)




### Define the parameters

MedicinalIngredientPerRegularBatch = data["MedicinalIngredientPerRegularBatch"] # shape: [], definition: Units of medicinal ingredients required to produce one regular batch

RehydrationProductPerRegularBatch = data["RehydrationProductPerRegularBatch"] # shape: [], definition: Units of rehydration product required to produce one regular batch

MedicinalIngredientPerPremiumBatch = data["MedicinalIngredientPerPremiumBatch"] # shape: [], definition: Units of medicinal ingredients required to produce one premium batch

RehydrationProductPerPremiumBatch = data["RehydrationProductPerPremiumBatch"] # shape: [], definition: Units of rehydration product required to produce one premium batch

TotalMedicinalIngredients = data["TotalMedicinalIngredients"] # shape: [], definition: Total available units of medicinal ingredients

TotalRehydrationProduct = data["TotalRehydrationProduct"] # shape: [], definition: Total available units of rehydration product

MinRegularBatches = data["MinRegularBatches"] # shape: [], definition: Minimum number of regular batches to produce

PeopleTreatedPerRegularBatch = data["PeopleTreatedPerRegularBatch"] # shape: [], definition: Number of people treated by one regular batch

PeopleTreatedPerPremiumBatch = data["PeopleTreatedPerPremiumBatch"] # shape: [], definition: Number of people treated by one premium batch



### Define the variables

RegularBatches = model.addVar(vtype=GRB.INTEGER, name="RegularBatches")

PremiumBatches = model.addVar(vtype=GRB.INTEGER, name="PremiumBatches")



### Define the constraints

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


### Define the objective

del.setObjective(
    PeopleTreatedPerRegularBatch * RegularBatches +
    PeopleTreatedPerPremiumBatch * PremiumBatches,
    GRB.MAXIMIZE


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
