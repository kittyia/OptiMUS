import os
import numpy as np
import json
from gurobipy import Model, GRB, quicksum

model = Model("OptimizationProblem")

with open("data.json", "r") as f:
    data = json.load(f)

# Define the parameters
NumProducts = data["NumProducts"]          # Number of products
NumMachines = data["NumMachines"]          # Number of machines
ProfitPerBatch = data["ProfitPerBatch"]    # Profit per batch of each product
TimeRequired = data["TimeRequired"]        # Time required on each machine for each product
MaxHours = data["MaxHours"]                # Maximum available hours per year for each machine

# Define the variables (nonnegative continuous)
ProduceBatches = model.addVars(NumProducts, lb=0, vtype=GRB.CONTINUOUS, name="ProduceBatches")

# Define the constraints (machine capacity constraints)
for m in range(NumMachines):
    model.addConstr(
        quicksum(TimeRequired[m][p] * ProduceBatches[p] for p in range(NumProducts)) 
        <= MaxHours[m],
        name=f"MachineCapacity_{m}"
    )

# Define the objective (maximize total profit)
model.setObjective(
    quicksum(ProfitPerBatch[p] * ProduceBatches[p] for p in range(NumProducts)),
    GRB.MAXIMIZE
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