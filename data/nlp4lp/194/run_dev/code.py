
import os
import numpy as np
import json 
from gurobipy import Model, GRB, quicksum


model = Model("OptimizationProblem")

with open("data.json", "r") as f:
    data = json.load(f)




### Define the parameters

MinCalcium = data["MinCalcium"] # shape: [], definition: Minimum required units of calcium per day

MinIron = data["MinIron"] # shape: [], definition: Minimum required units of iron per day

MilkCost = data["MilkCost"] # shape: [], definition: Cost of a glass of milk

MilkCalcium = data["MilkCalcium"] # shape: [], definition: Units of calcium in a glass of milk

MilkIron = data["MilkIron"] # shape: [], definition: Units of iron in a glass of milk

VegetableCost = data["VegetableCost"] # shape: [], definition: Cost of a plate of vegetables

VegetableCalcium = data["VegetableCalcium"] # shape: [], definition: Units of calcium in a plate of vegetables

VegetableIron = data["VegetableIron"] # shape: [], definition: Units of iron in a plate of vegetables



### Define the variables

MilkQty = model.addVar(vtype=GRB.INTEGER, name="MilkQty")

VegetableQty = model.addVar(vtype=GRB.INTEGER, name="VegetableQty")



### Define the constraints

model.addConstr(MilkCalcium * MilkQty + VegetableCalcium * VegetableQty >= MinCalcium)
model.addConstr(MilkIron * MilkQty + VegetableIron * VegetableQty >= MinIron)
model.addConstr(MilkQty >= 0)
model.addConstr(VegetableQty >= 0)


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
