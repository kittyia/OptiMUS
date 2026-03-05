import json
from gurobipy import *

# Load data
with open("data.json", "r") as f:
    data = json.load(f)

# Extract data
I = data["I"]
I_prime = data["I_prime"]
epsilon = data["epsilon"]
O = data["O"]
C = data["C"]
F_bar = data["F_bar"]
p = data["p"]
c_F = data["c_F"]
T = data["T"]
L = data["L"]
K = data["K"]

# Create model
model = Model("Order Consolidation")

# Variables
S = model.addVars(T, L, K, vtype=GRB.INTEGER, name="S")
S_prime = model.addVars(T, L, K, vtype=GRB.INTEGER, name="S_prime")
epsilon_vars = model.addVars(T, L, K, vtype=GRB.INTEGER, name="epsilon")
O_vars = model.addVars(L+1, K, vtype=GRB.INTEGER, name="O")

# Objective: Maximize multiorder hits
model.setObjective(quicksum(p[k] * epsilon_vars[t, s, k] for t in range(T) for s in range(L) for k in range(K)), GRB.MAXIMIZE)

# Constraints
for t in range(T):
    # Maximum flow constraint
    model.addConstr(quicksum(O_vars[s, k] for s in range(L+1) for k in range(K)) <= F_bar[str(t)], name=f"MaxFlow_{t}")

    # Pool size constraint
    model.addConstr(quicksum(S[t, s, k] for s in range(L) for k in range(K)) <= C[str(t)], name=f"PoolSize_{t}")

    # End-of-horizon constraint
    if t == T-1:
        model.addConstr(quicksum(S_prime[t, s, k] for s in range(L) for k in range(K)) == 0, name=f"EndHorizon_{t}")

    for s in range(L):
        for k in range(K):
            # Maximum stay constraint
            if t - s >= 0:
                model.addConstr(S_prime[t, s, k] <= S[t, s, k], name=f"MaxStay_{t}_{s}_{k}")

            # Update pool state
            if t - s >= 0:
                model.addConstr(S_prime[t, s, k] == S[t, s, k] - epsilon_vars[t, s, k] - O_vars[s, k], name=f"UpdatePool_{t}_{s}_{k}")

# Optimize model
model.optimize()

# Write solution
solution = {
    "variables": {v.varName: v.x for v in model.getVars()},
    "objective": model.objVal
}

with open("solution.json", "w") as f:
    json.dump(solution, f, indent=4)
