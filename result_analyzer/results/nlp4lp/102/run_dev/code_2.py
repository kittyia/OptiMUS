import json
import itertools

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

# We assume two decision variables (as per problem description)
# x[0] = number of demonstration 1
# x[1] = number of demonstration 2

# Constraint coefficients (A x <= b)
constraints = [
    (MintUsed, TotalMintAvailable),
    (ActiveIngredientUsed, TotalActiveIngredientAvailable),
    (BlackTarProduced, MaxBlackTarAllowed),
]

# Add non-negativity constraints implicitly: x1 >= 0, x2 >= 0

def is_feasible(x):
    # Non-negativity
    if any(xi < -1e-9 for xi in x):
        return False
    # Resource constraints
    for coeffs, rhs in constraints:
        if sum(coeffs[i] * x[i] for i in range(NumDemonstrations)) > rhs + 1e-9:
            return False
    return True

def objective(x):
    return sum(FoamProduced[i] * x[i] for i in range(NumDemonstrations))

# Generate candidate corner points
candidates = []

# 1. Origin
candidates.append([0.0, 0.0])

# 2. Intersections of each constraint with axes
for coeffs, rhs in constraints:
    for i in range(NumDemonstrations):
        if coeffs[i] != 0:
            x = [0.0, 0.0]
            x[i] = rhs / coeffs[i]
            candidates.append(x)

# 3. Intersections of pairs of constraints
for (coeffs1, rhs1), (coeffs2, rhs2) in itertools.combinations(constraints, 2):
    a1, b1 = coeffs1
    a2, b2 = coeffs2
    
    det = a1 * b2 - a2 * b1
    if abs(det) > 1e-9:
        x1 = (rhs1 * b2 - rhs2 * b1) / det
        x2 = (a1 * rhs2 - a2 * rhs1) / det
        candidates.append([x1, x2])

# Evaluate feasible candidates
optimal_value = None
for x in candidates:
    if is_feasible(x):
        val = objective(x)
        if (optimal_value is None) or (val > optimal_value):
            optimal_value = val

# Output result
with open("output_solution.txt", "w") as f:
    if optimal_value is not None:
        f.write(str(optimal_value))
    else:
        f.write("Infeasible")

print("Optimal Objective Value:", optimal_value)