import json
import pulp

# Create the LP maximization problem
model = pulp.LpProblem("OptimizationProblem", pulp.LpMaximize)

# Load data
with open("data.json", "r") as f:
    data = json.load(f)

# Parameters
NumDemonstrations = data["NumDemonstrations"]
MintUsed = data["MintUsed"]
ActiveIngredientUsed = data["ActiveIngredientUsed"]
FoamProduced = data["FoamProduced"]
BlackTarProduced = data["BlackTarProduced"]
TotalMintAvailable = data["TotalMintAvailable"]
TotalActiveIngredientAvailable = data["TotalActiveIngredientAvailable"]
MaxBlackTarAllowed = data["MaxBlackTarAllowed"]

# Decision variables (continuous and non-negative)
x = pulp.LpVariable.dicts("x", range(NumDemonstrations), lowBound=0, cat="Continuous")

# Objective: Maximize total minty foam produced
model += pulp.lpSum(FoamProduced[i] * x[i] for i in range(NumDemonstrations))

# Constraints
# Mint availability
model += pulp.lpSum(MintUsed[i] * x[i] for i in range(NumDemonstrations)) <= TotalMintAvailable

# Active ingredient availability
model += pulp.lpSum(ActiveIngredientUsed[i] * x[i] for i in range(NumDemonstrations)) <= TotalActiveIngredientAvailable

# Black tar limit
model += pulp.lpSum(BlackTarProduced[i] * x[i] for i in range(NumDemonstrations)) <= MaxBlackTarAllowed

# Solve the model
model.solve()

# Output optimal objective value
if pulp.LpStatus[model.status] == "Optimal":
    optimal_value = pulp.value(model.objective)
    print("Optimal Objective Value:", optimal_value)
    with open("output_solution.txt", "w") as f:
        f.write(str(optimal_value))
else:
    with open("output_solution.txt", "w") as f:
        f.write(pulp.LpStatus[model.status])