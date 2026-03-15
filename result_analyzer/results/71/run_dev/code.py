
import os
import numpy as np
import json 
from gurobipy import Model, GRB, quicksum


model = Model("OptimizationProblem")

with open("data.json", "r") as f:
    data = json.load(f)




### Define the parameters

MotionActivatedDropRate = data["MotionActivatedDropRate"] # shape: [], definition: Drop rate (drops per minute) of motion activated machine

MotionActivatedEnergyConsumption = data["MotionActivatedEnergyConsumption"] # shape: [], definition: Energy consumption (kWh) of motion activated machine

ManualDropRate = data["ManualDropRate"] # shape: [], definition: Drop rate (drops per minute) of manual machine

ManualEnergyConsumption = data["ManualEnergyConsumption"] # shape: [], definition: Energy consumption (kWh) of manual machine

MaxManualPercentage = data["MaxManualPercentage"] # shape: [], definition: Maximum percentage of machines that can be manual

MinMotionActivatedMachines = data["MinMotionActivatedMachines"] # shape: [], definition: Minimum number of motion activated machines

MinTotalDrops = data["MinTotalDrops"] # shape: [], definition: Minimum total drop delivery (drops per minute)

MaxTotalEnergy = data["MaxTotalEnergy"] # shape: [], definition: Maximum total energy consumption (kWh per minute)



### Define the variables

MotionActivatedMachines = model.addVar(vtype=GRB.INTEGER, name="MotionActivatedMachines")

ManualMachines = model.addVar(vtype=GRB.INTEGER, name="ManualMachines")



### Define the constraints

model.addConstr(MotionActivatedMachines >= MinMotionActivatedMachines)
model.addConstr(ManualMachines >= 0)
model.addConstr(
    ManualMachines <= MaxManualPercentage * (MotionActivatedMachines + ManualMachines)
)
model.addConstr(MotionActivatedDropRate * MotionActivatedMachines + ManualDropRate * ManualMachines >= MinTotalDrops)
model.addConstr(
    MotionActivatedEnergyConsumption * MotionActivatedMachines +
    ManualEnergyConsumption * ManualMachines
    <= MaxTotalEnergy
)


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
