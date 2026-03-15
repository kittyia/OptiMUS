
import os
import numpy as np
import json 
from gurobipy import Model, GRB, quicksum


model = Model("OptimizationProblem")

with open("data.json", "r") as f:
    data = json.load(f)




### Define the parameters

ProductionA = data["ProductionA"] # shape: [], definition: Production rate of Machine A in items per day

ProductionB = data["ProductionB"] # shape: [], definition: Production rate of Machine B in items per day

EnergyA = data["EnergyA"] # shape: [], definition: Energy consumption of Machine A in kWh per day

EnergyB = data["EnergyB"] # shape: [], definition: Energy consumption of Machine B in kWh per day

MinProduction = data["MinProduction"] # shape: [], definition: Minimum required production in items per day

MaxEnergy = data["MaxEnergy"] # shape: [], definition: Maximum available energy in kWh per day

MaxPercentB = data["MaxPercentB"] # shape: [], definition: Maximum percentage of machines that can be of type B

MinA = data["MinA"] # shape: [], definition: Minimum number of machines of type A



### Define the variables

numA = model.addVar(vtype=GRB.INTEGER, name="numA")

numB = model.addVar(vtype=GRB.INTEGER, name="numB")



### Define the constraints

model.addConstr(ProductionA * numA + ProductionB * numB >= MinProduction)
model.addConstr(EnergyA * numA + EnergyB * numB <= MaxEnergy)
model.addConstr(numB <= MaxPercentB * (numA + numB))
model.addConstr(numA >= MinA)
model.addConstr(numB >= 0)


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
