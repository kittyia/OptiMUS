import os
import numpy as np
import json
from gurobipy import Model, GRB, quicksum


model = Model("OptimizationProblem")

with open("data.json", "r") as f:
    data = json.load(f)


# Define the parameters
TransportCapacity = data["TransportCapacity"]
TransportCost = data["TransportCost"]
MinimumHydrogen = data["MinimumHydrogen"]
Budget = data["Budget"]
NumTransportMethods = data["NumTransportMethods"]


# Define the variables
NumTrips = model.addVars(NumTransportMethods, vtype=GRB.INTEGER, name="NumTrips")


# Define the constraints
model.addConstr(
    quicksum(TransportCapacity[m] * NumTrips[m] for m in range(NumTransportMethods))
    >= MinimumHydrogen
)

model.addConstr(
    quicksum(TransportCost[m] * NumTrips[m] for m in range(NumTransportMethods))
    <= Budget
)

# High pressure trips must be strictly less than liquefied tanker trips
model.addConstr(NumTrips[0] + 1 <= NumTrips[1])

for m in range(NumTransportMethods):
    model.addConstr(NumTrips[m] >= 0)


# Define the objective
model.setObjective(
    quicksum(NumTrips[i] for i in range(NumTransportMethods)),
    GRB.MINIMIZE
)


# Optimize the model
model.optimize()


# Output results safely
if model.status == GRB.OPTIMAL:
    print("Optimal Objective Value: ", model.ObjVal)
    with open("output_solution.txt", "w") as f:
        f.write(str(model.ObjVal))
else:
    print("Optimization ended with status:", model.status)
    with open("output_solution.txt", "w") as f:
        f.write(str(model.status))
``