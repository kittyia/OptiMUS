import os
import numpy as np
import json
from gurobipy import Model, GRB, quicksum


model = Model("OptimizationProblem")

with open("data.json", "r") as f:
    data = json.load(f)

# Define the parameters
HydrogenProductionA = data["HydrogenProductionA"]
PollutantOutputA = data["PollutantOutputA"]
HydrogenProductionB = data["HydrogenProductionB"]
PollutantOutputB = data["PollutantOutputB"]
MinHydrogenRequired = data["MinHydrogenRequired"]
MaxPollutantAllowed = data["MaxPollutantAllowed"]

# Define the variables
numGeneratorA = model.addVar(vtype=GRB.INTEGER, lb=0, name="numGeneratorA")
numGeneratorB = model.addVar(vtype=GRB.INTEGER, lb=0, name="numGeneratorB")

# Define the constraints
model.addConstr(
    HydrogenProductionA * numGeneratorA +
    HydrogenProductionB * numGeneratorB
    >= MinHydrogenRequired,
    name="HydrogenRequirement"
)

model.addConstr(
    PollutantOutputA * numGeneratorA +
    PollutantOutputB * numGeneratorB
    <= MaxPollutantAllowed,
    name="PollutantLimit"
)

# Define the objective (minimize total number of generators)
model.setObjective(numGeneratorA + numGeneratorB, GRB.MINIMIZE)

# Optimize the model
model.optimize()

# Output optimal objective value
if model.status == GRB.OPTIMAL:
    print("Optimal Objective Value: ", model.ObjVal)
    with open("output_solution.txt", "w") as f:
        f.write(str(model.ObjVal))
else:
    with open("output_solution.txt", "w") as f:
        f.write(str(model.status))