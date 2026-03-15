import os
import json
from gurobipy import Model, GRB, quicksum

# Create model
model = Model("DietProblem")

# Load data
with open("data.json", "r") as f:
    data = json.load(f)

# Normalize keys to lowercase to avoid KeyError due to capitalization
data = {k.lower(): v for k, v in data.items()}

# Parameters (robust to key capitalization)
Price = data["price"]            # list of length K
Demand = data["demand"]          # list of length M
Nutrition = data["nutrition"]    # K x M matrix

K = len(Price)
M = len(Demand)

# Decision variables
quantity = model.addVars(K, vtype=GRB.CONTINUOUS, lb=0.0, name="quantity")

# Nutrient constraints
for m in range(M):
    model.addConstr(
        quicksum(Nutrition[k][m] * quantity[k] for k in range(K)) >= Demand[m],
        name=f"Nutrient_{m}"
    )

# Objective: Minimize total cost
model.setObjective(
    quicksum(Price[k] * quantity[k] for k in range(K)),
    GRB.MINIMIZE
)

# Optimize
model.optimize()

# Output results
if model.status == GRB.OPTIMAL:
    solution = [quantity[k].x for k in range(K)]
    with open("output_solution.txt", "w") as f:
        f.write(json.dumps({"quantity": solution}))
else:
    with open("output_solution.txt", "w") as f:
        f.write(str(model.status))