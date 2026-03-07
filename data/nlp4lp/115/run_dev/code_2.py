import os
import numpy as np
import json
from gurobipy import Model, GRB, quicksum


model = Model("OptimizationProblem")

with open("data.json", "r") as f:
    data = json.load(f)


# Define the parameters
TimePerAnxietyUnit = data["TimePerAnxietyUnit"]  # Time for one unit of anxiety medication
TimePerAntidepressantUnit = data["TimePerAntidepressantUnit"]  # Time for one unit of anti-depressant
MinimumTotalUnits = data["MinimumTotalUnits"]  # Minimum total units required
MinimumAnxietyUnits = data["MinimumAnxietyUnits"]  # Minimum anxiety units required
MaximumAnxietyToAntidepressantRatio = data["MaximumAnxietyToAntidepressantRatio"]  # Max ratio


# Define the variables
AnxietyUnits = model.addVar(vtype=GRB.INTEGER, lb=0, name="AnxietyUnits")
AntidepressantUnits = model.addVar(vtype=GRB.INTEGER, lb=0, name="AntidepressantUnits")


# Define the constraints
model.addConstr(AnxietyUnits + AntidepressantUnits >= MinimumTotalUnits)
model.addConstr(AnxietyUnits >= MinimumAnxietyUnits)
model.addConstr(AnxietyUnits <= MaximumAnxietyToAntidepressantRatio * AntidepressantUnits)


# Define the objective
model.setObjective(
    TimePerAnxietyUnit * AnxietyUnits +
    TimePerAntidepressantUnit * AntidepressantUnits,
    GRB.MINIMIZE
)


# Optimize the model
model.optimize()


# Output optimal objective value
if model.status == GRB.OPTIMAL:
    print("Optimal Objective Value: ", model.objVal)
    with open("output_solution.txt", "w") as f:
        f.write(str(model.objVal))
else:
    with open("output_solution.txt", "w") as f:
        f.write(str(model.status))