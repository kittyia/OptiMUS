import os
import numpy as np
import json
from gurobipy import Model, GRB, quicksum

model = Model("OptimizationProblem")

with open("data.json", "r") as f:
    data = json.load(f)

# Define the parameters
NumMachines = data["NumMachines"]
NumParts = data["NumParts"]
TimeRequired = data["TimeRequired"]
MachineCosts = data["MachineCosts"]
Availability = data["Availability"]
Prices = data["Prices"]
MinBatches = data["MinBatches"]
StandardCost = data["StandardCost"]
OvertimeCost = data["OvertimeCost"]
OvertimeHour = data["OvertimeHour"]

# Define the variables

# Number of batches produced for each part
batches = model.addVars(NumParts, lb=0, name="batches")

# Machine 1 (index 0) labor split into regular and overtime hours
regular_1 = model.addVar(lb=0, ub=OvertimeHour, name="regular_1")
overtime_1 = model.addVar(lb=0, name="overtime_1")

# Define the constraints

# Time used on Machine 1 equals regular + overtime
model.addConstr(
    regular_1 + overtime_1 ==
    quicksum(TimeRequired[0][p] * batches[p] for p in range(NumParts)),
    name="Machine1_time_balance"
)

# Availability constraints for machines 2,...,M (index 1 to NumMachines-1)
for m in range(1, NumMachines):
    model.addConstr(
        quicksum(TimeRequired[m][p] * batches[p] for p in range(NumParts))
        <= Availability[m],
        name=f"Machine_{m+1}_availability"
    )

# Minimum production requirements
for p in range(NumParts):
    model.addConstr(
        batches[p] >= MinBatches[p],
        name=f"Min_batches_part_{p+1}"
    )

# Define the objective
model.setObjective(
    # Revenue
    quicksum(Prices[p] * batches[p] for p in range(NumParts))
    # Operating cost for machines 2,...,M
    - quicksum(
        MachineCosts[m] *
        quicksum(TimeRequired[m][p] * batches[p] for p in range(NumParts))
        for m in range(1, NumMachines)
    )
    # Labor cost for Machine 1
    - StandardCost * regular_1
    - OvertimeCost * overtime_1,
    GRB.MAXIMIZE
)

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