import json

# Load data
with open("data.json", "r") as f:
    data = json.load(f)

# Parameters
MinimumVitaminA = data["MinimumVitaminA"]
MinimumVitaminC = data["MinimumVitaminC"]

VitaminAPerCrabCake = data["VitaminAPerCrabCake"]
VitaminCPerCrabCake = data["VitaminCPerCrabCake"]

VitaminAPerLobsterRoll = data["VitaminAPerLobsterRoll"]
VitaminCPerLobsterRoll = data["VitaminCPerLobsterRoll"]

UnsaturatedFatPerCrabCake = data["UnsaturatedFatPerCrabCake"]
UnsaturatedFatPerLobsterRoll = data["UnsaturatedFatPerLobsterRoll"]

MaximumLobsterFraction = data["MaximumLobsterFraction"]

# Brute-force search since problem size is very small
best_objective = None

# Reasonable upper bound for search
max_meals = 500

for CrabCakes in range(max_meals + 1):
    for LobsterRolls in range(max_meals + 1):

        # Vitamin constraints
        if (VitaminAPerCrabCake * CrabCakes +
            VitaminAPerLobsterRoll * LobsterRolls < MinimumVitaminA):
            continue

        if (VitaminCPerCrabCake * CrabCakes +
            VitaminCPerLobsterRoll * LobsterRolls < MinimumVitaminC):
            continue

        # Lobster fraction constraint
        if CrabCakes + LobsterRolls > 0:
            if LobsterRolls > MaximumLobsterFraction * (CrabCakes + LobsterRolls):
                continue

        # Objective: minimize unsaturated fat
        objective = (UnsaturatedFatPerCrabCake * CrabCakes +
                     UnsaturatedFatPerLobsterRoll * LobsterRolls)

        if best_objective is None or objective < best_objective:
            best_objective = objective

# Output result
with open("output_solution.txt", "w") as f:
    if best_objective is not None:
        f.write(str(best_objective))
    else:
        f.write("Infeasible")