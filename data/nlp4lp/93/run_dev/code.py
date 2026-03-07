
import os
import numpy as np
import json 
from gurobipy import Model, GRB, quicksum


model = Model("OptimizationProblem")

with open("data.json", "r") as f:
    data = json.load(f)




### Define the parameters

TotalToothMedication = data["TotalToothMedication"] # shape: [], definition: Total units of tooth medication available for making bones

ToothMedicationPerSmallBone = data["ToothMedicationPerSmallBone"] # shape: [], definition: Units of tooth medication required to make one small bone

MeatPerSmallBone = data["MeatPerSmallBone"] # shape: [], definition: Units of meat required to make one small bone

ToothMedicationPerLargeBone = data["ToothMedicationPerLargeBone"] # shape: [], definition: Units of tooth medication required to make one large bone

MeatPerLargeBone = data["MeatPerLargeBone"] # shape: [], definition: Units of meat required to make one large bone

MinProportionSmallBones = data["MinProportionSmallBones"] # shape: [], definition: Minimum proportion of bones that must be small

MinLargeBones = data["MinLargeBones"] # shape: [], definition: Minimum number of large bones to be made



### Define the variables

SmallBones = model.addVar(vtype=GRB.INTEGER, name="SmallBones")

LargeBones = model.addVar(vtype=GRB.INTEGER, name="LargeBones")



### Define the constraints

model.addConstr(
    ToothMedicationPerSmallBone * SmallBones +
    ToothMedicationPerLargeBone * LargeBones
    <= TotalToothMedication
)
model.addConstr(SmallBones >= MinProportionSmallBones * (SmallBones + LargeBones))
model.addConstr(LargeBones >= MinLargeBones)


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
