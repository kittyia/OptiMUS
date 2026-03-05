import json
from gurobipy import Model, GRB, quicksum, LinExpr

# 1. Load data
with open("data.json", "r") as f:
    data = json.load(f)

S = data["ShipOptions"]           # number of ship options
P = data["PriorDays"]             # number of prior days
T = data["PlanningHorizon"]       # planning horizon length
capacity = data["LockerCapacity"] # locker capacity

dwell = data["DwellTimeProb"]          # shape [S][T][T]
dwell_prior = data["DwellTimeProbPrior"]  # shape [S][P][T]
initial_pkgs = data["PackagesInLockerDayZero"]  # shape [S][P]
demand = data["Demand"]                     # shape [S][T]

# 2. Build model
model = Model("AmazonLockerThroughput")

# Decision variables: x[s,t] – packages of ship option s accepted on day t
x = {}
for s in range(S):
    for t in range(T):
        var_name = f"x_{s}_{t}"
        x[s, t] = model.addVar(
            vtype=GRB.INTEGER,
            lb=0,
            ub=demand[s][t],   # cannot exceed demand
            name=var_name
        )

model.update()

# 3. Capacity constraints for each day t
for t in range(T):
    # Expected occupancy from newly accepted packages
    expr = quicksum(dwell[s][v][t] * x[s, v]
                    for s in range(S)
                    for v in range(t + 1))   # only deliveries up to day t

    # Expected occupancy from packages already in locker at day 0 (constant)
    constant = sum(dwell_prior[s][v][t] * initial_pkgs[s][v]
                   for s in range(S)
                   for v in range(P))

    model.addConstr(expr + constant <= capacity,
                    name=f"capacity_{t}")

# 4. Objective: maximise total accepted packages
model.setObjective(
    quicksum(x[s, t] for s in range(S) for t in range(T)),
    GRB.MAXIMIZE
)

# 5. Solve
model.optimize()

# 6. Write solution
solution = {
    "variables": {var.VarName: var.X for var in model.getVars()},
    "objective": model.objVal if model.SolCount > 0 else None
}

with open("solution.json", "w") as f:
    json.dump(solution, f, indent=4)
