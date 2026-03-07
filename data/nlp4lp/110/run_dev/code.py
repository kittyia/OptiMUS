
import os
import numpy as np
import json 
from gurobipy import Model, GRB, quicksum


model = Model("OptimizationProblem")

with open("data.json", "r") as f:
    data = json.load(f)




### Define the parameters

Machine1HeartDeliveryRate = data["Machine1HeartDeliveryRate"] # shape: [], definition: Units of medicine delivered to the heart per minute by machine 1

Machine1BrainDeliveryRate = data["Machine1BrainDeliveryRate"] # shape: [], definition: Units of medicine delivered to the brain per minute by machine 1

Machine1WasteRate = data["Machine1WasteRate"] # shape: [], definition: Units of waste produced per minute by machine 1

Machine2HeartDeliveryRate = data["Machine2HeartDeliveryRate"] # shape: [], definition: Units of medicine delivered to the heart per minute by machine 2

Machine2BrainDeliveryRate = data["Machine2BrainDeliveryRate"] # shape: [], definition: Units of medicine delivered to the brain per minute by machine 2

Machine2WasteRate = data["Machine2WasteRate"] # shape: [], definition: Units of waste produced per minute by machine 2

HeartMedicineMax = data["HeartMedicineMax"] # shape: [], definition: Maximum units of medicine that can be received by the heart

BrainMedicineMin = data["BrainMedicineMin"] # shape: [], definition: Minimum units of medicine that should be received by the brain



### Define the variables

x1 = model.addVar(vtype=GRB.CONTINUOUS, name="x1")

x2 = model.addVar(vtype=GRB.CONTINUOUS, name="x2")



### Define the constraints

model.addConstr(Machine1HeartDeliveryRate * x1 + Machine2HeartDeliveryRate * x2 <= HeartMedicineMax)
model.addConstr(Machine1BrainDeliveryRate * x1 + Machine2BrainDeliveryRate * x2 >= BrainMedicineMin)
model.addConstr(x1 >= 0)
model.addConstr(x2 >= 0)


### Define the objective

model.setObjective(Machine1WasteRate * x1 + Machine2WasteRate * x2, GRB.MINIMIZE)


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
