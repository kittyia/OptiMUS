import os
import json
from gurobipy import Model, GRB, quicksum

# Create model
model = Model("CuttingStockProblem")

# Load data
with open("data.json", "r") as f:
    data = json.load(f)

# Parameters
large_roll_width = data["large_roll_width"]
demands = data["demands"]
roll_width_options = data["roll_width_options"]
patterns = data["patterns"]

# Derived dimensions
N = len(patterns)          # Number of cutting patterns
M = len(demands)           # Number of roll types

# Decision variables
# amount[i] = number of large rolls cut using pattern i
amount = model.addVars(N, vtype=GRB.INTEGER, lb=0, name="amount")

# Demand satisfaction constraints
for j in range(M):
    model.addConstr(
        quicksum(patterns[i][j] * amount[i] for i in range(N)) >= demands[j],
        name=f"demand_{j}"
    )

# Objective: Minimize total large rolls used
model.setObjective(quicksum(amount[i] for i in range(N)), GRB.MINIMIZE)

# Optimize
model.optimize()

# Output results
if model.status == GRB.OPTIMAL:
    solution = {
        "patterns": [
            {
                "pattern": patterns[i],
                "amount": int(amount[i].x)
            }
            for i in range(N) if amount[i].x > 0
        ],
        "total_large_rolls_used": int(model.objVal)
    }

    with open("output_solution.txt", "w") as f:
        json.dump(solution, f, indent=4)

    print("Optimal Objective Value:", model.objVal)
else:
    with open("output_solution.txt", "w") as f:
        f.write(str(model.status))