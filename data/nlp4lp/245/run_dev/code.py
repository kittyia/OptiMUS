
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

numAutoElectricJacks = model.addVar(vtype=GRB.INTEGER, name="numAutoElectricJacks")

numGasPoweredJacks = model.addVar(vtype=GRB.INTEGER, name="numGasPoweredJacks")



### Define the constraints

model.addConstr(AutoElectricElectricityUsage * numAutoElectricJacks <= MaxElectricityUnits)
model.addConstr(GasPoweredGasUsage * numGasPoweredJacks <= MaxGasUnits)
model.addConstr(numAutoElectricJacks >= 0)
model.addConstr(numGasPoweredJacks >= 0)


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
