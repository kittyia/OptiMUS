import json
from gurobipy import *

# Load data
with open("data.json", "r") as f:
    data = json.load(f)

# Extract parameters
ShipOptions = data["ShipOptions"]
PriorDays = data["PriorDays"]
PlanningHorizon = data["PlanningHorizon"]
LockerCapacity = data["LockerCapacity"]
DwellTimeProb = data["DwellTimeProb"]
DwellTimeProbPrior = data["DwellTimeProbPrior"]
PackagesInLockerDayZero = data["PackagesInLockerDayZero"]
Demand = data["Demand"]

# Create model
model = Model("AmazonLockerThroughput")

# Decision variables
x = model.addVars(ShipOptions, PlanningHorizon, vtype=GRB.INTEGER, name="x")

# Objective: Maximize throughput
model.setObjective(quicksum(x[s, t] for s in range(ShipOptions) for t in range(PlanningHorizon)), GRB.MAXIMIZE)

# Constraints
# 1. Locker capacity constraint
for t in range(PlanningHorizon):
    model.addConstr(
        quicksum(
            DwellTimeProb[s][v][t] * x[s, v] for s in range(ShipOptions) for v in range(t + 1)
        ) + quicksum(
            DwellTimeProbPrior[s][v][t] * PackagesInLockerDayZero[s][v] for s in range(ShipOptions) for v in range(PriorDays)
        ) <= LockerCapacity,
        name=f"LockerCapacity_{t}"
    )

# 2. Demand constraint
for s in range(ShipOptions):
    for t in range(PlanningHorizon):
        model.addConstr(x[s, t] <= Demand[s][t], name=f"Demand_{s}_{t}")

# 3. Non-negativity constraint
for s in range(ShipOptions):
    for t in range(PlanningHorizon):
        model.addConstr(x[s, t] >= 0, name=f"NonNegativity_{s}_{t}")

# Optimize model
model.optimize()

# Write solution to solution.json
solution = {
    "variables": {f"x_{s}_{t}": x[s, t].X for s in range(ShipOptions) for t in range(PlanningHorizon)},
    "objective": model.objVal
}

with open("solution.json", "w") as f:
    json.dump(solution, f, indent=4)
