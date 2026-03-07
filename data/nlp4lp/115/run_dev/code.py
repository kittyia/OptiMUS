
import os
import numpy as np
import json 
from gurobipy import Model, GRB, quicksum


model = Model("OptimizationProblem")

with open("data.json", "r") as f:
    data = json.load(f)




### Define the parameters

TimePerAnxietyUnit = data["TimePerAnxietyUnit"] # shape: [], definition: Time it takes for one unit of anxiety medication to be effective

TimePerAntidepressantUnit = data["TimePerAntidepressantUnit"] # shape: [], definition: Time it takes for one unit of anti-depressant to be effective

MinimumTotalUnits = data["MinimumTotalUnits"] # shape: [], definition: Minimum total units of medication the patient must take

MinimumAnxietyUnits = data["MinimumAnxietyUnits"] # shape: [], definition: Minimum units of anxiety medication the patient must take

MaximumAnxietyToAntidepressantRatio = data["MaximumAnxietyToAntidepressantRatio"] # shape: [], definition: Maximum ratio of anxiety medication units to anti-depressant units



### Define the variables

AnxietyUnits = model.addVar(vtype=GRB.INTEGER, name="AnxietyUnits")

AntidepressantUnits = model.addVar(vtype=GRB.INTEGER, name="AntidepressantUnits")



### Define the constraints

model.addConstr(AnxietyUnits + AntidepressantUnits >= MinimumTotalUnits)
model.addConstr(AnxietyUnits >= MinimumAnxietyUnits)
model.addConstr(AnxietyUnits <= MaximumAnxietyToAntidepressantRatio * AntidepressantUnits])


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
