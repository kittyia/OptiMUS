
import os
import numpy as np
import json 
from gurobipy import Model, GRB, quicksum


model = Model("OptimizationProblem")

with open("data.json", "r") as f:
    data = json.load(f)




### Define the parameters

NitrogenA = data["NitrogenA"] # shape: [], definition: Units of nitrogen per kg of fertilizer A

NitrogenB = data["NitrogenB"] # shape: [], definition: Units of nitrogen per kg of fertilizer B

PhosphoricAcidA = data["PhosphoricAcidA"] # shape: [], definition: Units of phosphoric acid per kg of fertilizer A

PhosphoricAcidB = data["PhosphoricAcidB"] # shape: [], definition: Units of phosphoric acid per kg of fertilizer B

VitaminAA = data["VitaminAA"] # shape: [], definition: Units of vitamin A per kg of fertilizer A

VitaminAB = data["VitaminAB"] # shape: [], definition: Units of vitamin A per kg of fertilizer B

VitaminDA = data["VitaminDA"] # shape: [], definition: Units of vitamin D per kg of fertilizer A

VitaminDB = data["VitaminDB"] # shape: [], definition: Units of vitamin D per kg of fertilizer B

MinNitrogen = data["MinNitrogen"] # shape: [], definition: Minimum required units of nitrogen in the nutrition

MinPhosphoricAcid = data["MinPhosphoricAcid"] # shape: [], definition: Minimum required units of phosphoric acid in the nutrition

MaxVitaminA = data["MaxVitaminA"] # shape: [], definition: Maximum allowed units of vitamin A in the nutrition



### Define the variables

amountOfA = model.addVar(vtype=GRB.CONTINUOUS, name="amountOfA")

amountOfB = model.addVar(vtype=GRB.CONTINUOUS, name="amountOfB")



### Define the constraints

model.addConstr(NitrogenA * amountOfA + NitrogenB * amountOfB >= MinNitrogen)
model.addConstr(PhosphoricAcidA * amountOfA + PhosphoricAcidB * amountOfB >= MinPhosphoricAcid)
model.addConstr(VitaminAA * amountOfA + VitaminAB * amountOfB <= MaxVitaminA)
model.addConstr(amountOfA >= 0)
model.addConstr(amountOfB >= 0)


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
