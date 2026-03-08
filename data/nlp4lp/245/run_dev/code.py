
import os
import numpy as np
import json 
from gurobipy import Model, GRB, quicksum


model = Model("OptimizationProblem")

with open("data.json", "r") as f:
    data = json.load(f)




### Define the parameters

AutoElectricProcessingRate = data["AutoElectricProcessingRate"] # shape: [], definition: The number of cars processed per hour by one automatic electric jack.

AutoElectricElectricityUsage = data["AutoElectricElectricityUsage"] # shape: [], definition: Units of electricity used per hour by one automatic electric jack.

GasPoweredProcessingRate = data["GasPoweredProcessingRate"] # shape: [], definition: The number of cars processed per hour by one gas-powered jack.

GasPoweredGasUsage = data["GasPoweredGasUsage"] # shape: [], definition: Units of gas used per hour by one gas-powered jack.

MaxAutoElectricJacks = data["MaxAutoElectricJacks"] # shape: [], definition: The maximum number of automatic electric jacks that can be used.

MaxElectricityUnits = data["MaxElectricityUnits"] # shape: [], definition: The maximum units of electricity available.

MaxGasUnits = data["MaxGasUnits"] # shape: [], definition: The maximum units of gas available.



### Define the variables

AutoElectricJacks = model.addVar(vtype=GRB.INTEGER, name="AutoElectricJacks")

GasPoweredJacks = model.addVar(vtype=GRB.INTEGER, name="GasPoweredJacks")



### Define the constraints

model.addConstr(6 * AutoElectricJacks <= MaxElectricityUnits)
model.addConstr(7 * GasPoweredJacks <= MaxGasUnits)
model.addConstr(AutoElectricJacks >= 0)
model.addConstr(GasPoweredJacks >= 0)


### Define the objective

model.setObjective(
    AutoElectricProcessingRate * AutoElectricJacks +
    GasPoweredProcessingRate * GasPoweredJacks,
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
