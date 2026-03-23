
import os
import numpy as np
import json 
from gurobipy import Model, GRB, quicksum


model = Model("OptimizationProblem")

with open("data.json", "r") as f:
    data = json.load(f)




### Define the parameters

HydrogenProductionA = data["HydrogenProductionA"] # shape: [], definition: Amount of hydrogen produced per day by generator A

PollutantOutputA = data["PollutantOutputA"] # shape: [], definition: Amount of pollutants produced per day by generator A

HydrogenProductionB = data["HydrogenProductionB"] # shape: [], definition: Amount of hydrogen produced per day by generator B

PollutantOutputB = data["PollutantOutputB"] # shape: [], definition: Amount of pollutants produced per day by generator B

MinHydrogenRequired = data["MinHydrogenRequired"] # shape: [], definition: Minimum hydrogen required per day

MaxPollutantAllowed = data["MaxPollutantAllowed"] # shape: [], definition: Maximum pollutants allowed per day



### Define the variables

numGeneratorA = model.addVar(vtype=GRB.INTEGER, name="numGeneratorA")

numGeneratorB = model.addVar(vtype=GRB.INTEGER, name="numGeneratorB")



### Define the constraints

model.addConstr(HydrogenProductionA * numGeneratorA + HydrogenProductionB * numGeneratorB >= MinHydrogenRequired)
model.addConstr(PollutantOutputA * numGeneratorA + PollutantOutputB * numGeneratorB <= MaxPollutantAllowed)
model.addConstr(numGeneratorA >= 0)
model.addConstr(numGeneratorB >= 0)


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
