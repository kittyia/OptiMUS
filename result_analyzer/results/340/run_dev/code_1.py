import os
import numpy as np
import json
from gurobipy import Model, GRB, quicksum


model = Model("OptimizationProblem")

with open("data.json", "r") as f:
    data = json.load(f)

### Define the parameters

M = data["M"]  # Number of machines
P = data["P"]  # Number of parts

TimeRequired = data["TimeRequired"]      # shape: [M][P]
MachineCosts = data["MachineCosts"]      # shape: [M]
Availability = data["Availability"]      # shape: [M]
Prices = data["Prices"]                  # shape: [P]
MinBatches = data["MinBatches"]          # shape: [P]

### Define the variables

batches = model.addVars(P, lb=0, vtype=GRB.CONTINUOUS, name="batches")

### Define the constraints

# Machine availability constraints except last two machines
for m in range(M - 2):
    model.addConstr(
        quicksum(TimeRequired[m][p] * batches[p] for p in range(P))
        <= Availability[m],
        name=f"Machine_{m}_capacity"
    )

# Shared availability constraint for last two machines
model.addConstr(
    quicksum(TimeRequired[M - 2][p] * batches[p] for p in range(P)) +
    quicksum(TimeRequired[M - 1][p] * batches[p] for p in range(P))
    <= Availability[M - 2] + Availability[M - 1],
    name="Shared_capacity"
)

# Minimum production constraints
for p in range(P):
    model.addConstr(
        batches[p] >= MinBatches[p],
        name=f"Min_batches_{p}"
    )

### Define the objective

model.setObjective(
    quicksum(Prices[p] * batches[p] for p in range(P))
    - quicksum(
        MachineCosts[m] *
        quicksum(TimeRequired[m][p] * batches[p] for p in range(P))
        for m in range(M)
    ),
    GRB.MAXIMIZE
)

### Optimize the model

model.optimize()

### Output results

if model.status == GRB.OPTIMAL:
    solution = {
        "batches": [batches[p].X for p in range(P)],
        "total_profit": model.objVal
    }
    with open("output_solution.txt", "w") as f:
        f.write(json.dumps(solution))
else:
    with open("output_solution.txt", "w") as f:
        f.write(str(model.status))
``