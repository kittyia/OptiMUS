import json
from scipy.optimize import linprog

# Load data
with open("data.json", "r") as f:
    data = json.load(f)

# Parameters
TotalBudget = data["TotalBudget"]
ProfitPerDollarCondos = data["ProfitPerDollarCondos"]
ProfitPerDollarDetachedHouses = data["ProfitPerDollarDetachedHouses"]
MinimumPercentageCondos = data["MinimumPercentageCondos"]
MinimumInvestmentDetachedHouses = data["MinimumInvestmentDetachedHouses"]

# Objective function (linprog minimizes, so negate to maximize)
c = [
    -ProfitPerDollarCondos,
    -ProfitPerDollarDetachedHouses
]

# Constraints (A_ub x <= b_ub)

A_ub = [
    [1, 1],  # Budget constraint: x + y <= TotalBudget
    [-(1 - MinimumPercentageCondos), MinimumPercentageCondos],  # Condo percentage constraint
    [0, -1]  # Minimum detached houses investment: -y <= -MinimumInvestmentDetachedHouses
]

b_ub = [
    TotalBudget,
    0,
    -MinimumInvestmentDetachedHouses
]

# Variable bounds (x >= 0, y >= 0)
bounds = [
    (0, None),  # InvestmentCondos
    (0, None)   # InvestmentDetachedHouses
]

# Solve the LP
result = linprog(c, A_ub=A_ub, b_ub=b_ub, bounds=bounds, method="highs")

# Output results
if result.success:
    optimal_value = -result.fun  # Convert back to maximization
    print("Optimal Objective Value:", optimal_value)
    with open("output_solution.txt", "w") as f:
        f.write(str(optimal_value))
else:
    with open("output_solution.txt", "w") as f:
        f.write(result.message)