
import os
import numpy as np
import json 
from gurobipy import Model, GRB, quicksum


model = Model("OptimizationProblem")

with open("data.json", "r") as f:
    data = json.load(f)




### Define the parameters

DualStampRate = data["DualStampRate"] # shape: [], definition: Stamping rate of dual model stamping machine (letters per minute)

DualGlueUsage = data["DualGlueUsage"] # shape: [], definition: Glue usage rate of dual model stamping machine (units per minute)

SingleStampRate = data["SingleStampRate"] # shape: [], definition: Stamping rate of single model stamping machine (letters per minute)

SingleGlueUsage = data["SingleGlueUsage"] # shape: [], definition: Glue usage rate of single model stamping machine (units per minute)

MinTotalLetters = data["MinTotalLetters"] # shape: [], definition: Minimum total letters to be stamped per minute

MaxGlueUsage = data["MaxGlueUsage"] # shape: [], definition: Maximum total glue usage per minute



### Define the variables

DualMachines = model.addVar(vtype=GRB.INTEGER, name="DualMachines")

SingleMachines = model.addVar(vtype=GRB.INTEGER, name="SingleMachines")



### Define the constraints

model.addConstr(DualStampRate * DualMachines + SingleStampRate * SingleMachines >= MinTotalLetters)
model.addConstr(DualGlueUsage * DualMachines + SingleGlueUsage * SingleMachines <= MaxGlueUsage)
model.addConstr(SingleMachines >= DualMachines + 1)
model.addConstr(DualMachines >= 0)
model.addConstr(SingleMachines >= 0)


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
