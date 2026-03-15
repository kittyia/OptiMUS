import json

# Load data
with open("data.json", "r") as f:
    data = json.load(f)

# Parameters
TotalBudget = data["TotalBudget"]
ProfitPerDollarCondos = data["ProfitPerDollarCondos"]
ProfitPerDollarDetachedHouses = data["ProfitPerDollarDetachedHouses"]
MinimumPercentageCondos = data["MinimumPercentageCondos"]
MinimumInvestmentDetachedHouses = data["MinimumInvestmentDetachedHouses"]

# Let:
# x = investment in condos
# y = investment in detached houses

# Constraints:
# 1) x + y <= TotalBudget
# 2) x >= MinimumPercentageCondos * (x + y)
# 3) y >= MinimumInvestmentDetachedHouses
# 4) x, y >= 0

# Rewrite constraint (2):
# x >= p(x + y)
# x >= px + py
# x - px >= py
# (1 - p)x >= py
# y <= ((1 - p) / p) * x

p = MinimumPercentageCondos
ratio = (1 - p) / p  # y <= ratio * x

# To maximize profit (since profit per dollar of y >= profit per dollar of x),
# we push y as large as possible.
# So optimal occurs at:
# 1) x + y = TotalBudget
# 2) y = ratio * x

# Solve:
# x + ratio*x = TotalBudget
# x(1 + ratio) = TotalBudget
# x = TotalBudget / (1 + ratio)
# y = ratio * x

x = TotalBudget / (1 + ratio)
y = ratio * x

# Ensure minimum detached investment constraint is satisfied
if y < MinimumInvestmentDetachedHouses:
    y = MinimumInvestmentDetachedHouses
    x = TotalBudget - y

# Compute optimal profit
optimal_value = (
    ProfitPerDollarCondos * x +
    ProfitPerDollarDetachedHouses * y
)

# Output result
with open("output_solution.txt", "w") as f:
    f.write(str(optimal_value))

print("Optimal Objective Value:", optimal_value)