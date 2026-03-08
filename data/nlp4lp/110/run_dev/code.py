
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

Machine1Minutes = model.addVar(vtype=GRB.CONTINUOUS, name="Machine1Minutes")

Machine2Minutes = model.addVar(vtype=GRB.CONTINUOUS, name="Machine2Minutes")



### Define the constraints

model.addConstr(Machine1HeartDeliveryRate * Machine1Minutes + Machine2HeartDeliveryRate * Machine2Minutes <= HeartMedicineMax)
model.addConstr(Machine1BrainDeliveryRate * Machine1Minutes + Machine2BrainDeliveryRate * Machine2Minutes >= BrainMedicineMin)
model.addConstr(Machine1Minutes >= 0)
model.addConstr(Machine2Minutes >= 0)


### Define the objective

model.setObjective(
    Machine1WasteRate * Machine1Minutes +
    Machine2WasteRate * Machine2Minutes,
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
