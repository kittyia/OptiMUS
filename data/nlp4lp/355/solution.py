import json
from gurobipy import Model, GRB

# Read inputs from JSON file
with open("data.json", "r") as f:
    inputs = json.load(f)

ShipOptions = inputs["ShipOptions"]
PriorDays = inputs["PriorDays"]
PlanningHorizon = inputs["PlanningHorizon"]
LockerCapacity = inputs["LockerCapacity"]
DwellTimeProb = inputs["DwellTimeProb"]
DwellTimeProbPrior = inputs["DwellTimeProbPrior"]
PackagesInLockerDayZero = inputs["PackagesInLockerDayZero"]
Demand = inputs["Demand"]

# Create a new model
model = Model("LockerThroughputOptimization")

# Decision variables
y = model.addVars(ShipOptions, PlanningHorizon, vtype=GRB.CONTINUOUS, name="y")
x = model.addVars(ShipOptions, PlanningHorizon, vtype=GRB.CONTINUOUS, name="x")

# Objective function: Maximize the total number of packages delivered to the locker
model.setObjective(
    sum(y[s, t] for s in range(ShipOptions) for t in range(PlanningHorizon)),
    GRB.MAXIMIZE,
)

# Constraints
for t in range(PlanningHorizon):
    model.addConstr(
        sum(
            DwellTimeProb[s][v][t] * y[s, v]
            for s in range(ShipOptions)
            for v in range(t + 1)
        )
        + sum(
            DwellTimeProbPrior[s][v][t] * PackagesInLockerDayZero[s][v]
            for s in range(ShipOptions)
            for v in range(PriorDays)
        )
        <= LockerCapacity,
        name=f"LockerCapacityConstraint_{t}",
    )

for s in range(ShipOptions):
    for t in range(PlanningHorizon):
        model.addConstr(y[s, t] <= Demand[s][t], name=f"DemandConstraint_{s}_{t}")

for s in range(ShipOptions):
    for t in range(PlanningHorizon):
        model.addConstr(
            sum(DwellTimeProb[s][v][t] * y[s, v] for v in range(t + 1))
            + sum(
                DwellTimeProb[s][v][t] * PackagesInLockerDayZero[s][v]
                for v in range(ShipOptions)
            )
            == x[s, t],
            name=f"ReservationConstraint_{s}_{t}",
        )

for s in range(ShipOptions):
    for t in range(PlanningHorizon):
        model.addConstr(x[s, t] >= 0, name=f"NonNegative_x_{s}_{t}")
        model.addConstr(y[s, t] >= 0, name=f"NonNegative_y_{s}_{t}")

# Optimize the model
model.optimize()

# Extract results
if model.status == GRB.OPTIMAL:
    print(f"Obj: {model.objVal}")
    from pathlib import Path

    Path("obj.txt").write_text(str(model.objVal))
else:
    print("No optimal solution found.")
