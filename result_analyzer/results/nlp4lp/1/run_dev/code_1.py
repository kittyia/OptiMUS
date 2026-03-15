import json
import pulp

# Create the LP problem (maximize objective)
model = pulp.LpProblem("OptimizationProblem", pulp.LpMaximize)

# Load data
with open("data.json", "r") as f:
    data = json.load(f)

# Parameters
TotalBudget = data["TotalBudget"]
ProfitPerDollarCondos = data["ProfitPerDollarCondos"]
ProfitPerDollarDetachedHouses = data["ProfitPerDollarDetachedHouses"]
MinimumPercentageCondos = data["MinimumPercentageCondos"]
MinimumInvestmentDetachedHouses = data["MinimumInvestmentDetachedHouses"]

# Decision Variables
InvestmentCondos = pulp.LpVariable("InvestmentCondos", lowBound=0, cat="Continuous")
InvestmentDetachedHouses = pulp.LpVariable("InvestmentDetachedHouses", lowBound=0, cat="Continuous")

# Constraints
model += InvestmentCondos + InvestmentDetachedHouses <= TotalBudget
model += InvestmentCondos >= MinimumPercentageCondos * (InvestmentCondos + InvestmentDetachedHouses)
model += InvestmentDetachedHouses >= MinimumInvestmentDetachedHouses

# Objective Function
model += (
    ProfitPerDollarCondos * InvestmentCondos +
    ProfitPerDollarDetachedHouses * InvestmentDetachedHouses
)

# Solve the model
model.solve()

# Output results
if pulp.LpStatus[model.status] == "Optimal":
    optimal_value = pulp.value(model.objective)
    print("Optimal Objective Value:", optimal_value)
    with open("output_solution.txt", "w") as f:
        f.write(str(optimal_value))
else:
    with open("output_solution.txt", "w") as f:
        f.write(pulp.LpStatus[model.status])