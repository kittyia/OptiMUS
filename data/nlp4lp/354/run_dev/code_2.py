import os
import numpy as np
import json
from gurobipy import Model, GRB, quicksum

model = Model("OptimizationProblem")

with open("data.json", "r") as f:
    data = json.load(f)

# Define the parameters
large_roll_width = data["large_roll_width"]
demands = data["demands"]                  # length M
roll_width_options = data["roll_width_options"]
patterns = data["patterns"]                # size N x M

# Define dimensions
N = len(patterns)          # number of cutting patterns
M = len(demands)           # number of roll types

# Define the variables
amount = model.addVars(N, vtype=GRB.INTEGER, lb=0, name="amount")

# Define the constraints

# Demand satisfaction constraints
for j in range(M):
    model.addConstr(
        quicksum(patterns[i][j] * amount[i] for i in range(N)) >= demands[j],
        name=f"demand_{j}"
    )

# Define the objective
model.setObjective(quicksum(amount[i] for i in range(N)), GRB.MINIMIZE)

# Optimize the model
model.optimize()

# Output optimal objective value
if model.status == GRB.OPTIMAL:
    print("Optimal Objective Value:", model.objVal)
    with open("output_solution.txt", "w") as f:
        f.write(str(model.objVal))
else:
    with open("output_solution.txt", "w") as f:
        f.write(str(model.status))