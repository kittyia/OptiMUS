import json

# Load data
with open("data.json", "r") as f:
    data = json.load(f)

# Define parameters
NumDemonstrations = data["NumDemonstrations"]
MintUsed = data["MintUsed"]
ActiveIngredientUsed = data["ActiveIngredientUsed"]
FoamProduced = data["FoamProduced"]
BlackTarProduced = data["BlackTarProduced"]
TotalMintAvailable = data["TotalMintAvailable"]
TotalActiveIngredientAvailable = data["TotalActiveIngredientAvailable"]
MaxBlackTarAllowed = data["MaxBlackTarAllowed"]

# Since the problem is small (2 demonstrations), solve by brute force search
best_objective = -1
best_solution = None

# Compute safe upper bounds for each demonstration
max_bounds = []
for d in range(NumDemonstrations):
    bound_mint = TotalMintAvailable // MintUsed[d] if MintUsed[d] > 0 else float('inf')
    bound_active = TotalActiveIngredientAvailable // ActiveIngredientUsed[d] if ActiveIngredientUsed[d] > 0 else float('inf')
    bound_tar = MaxBlackTarAllowed // BlackTarProduced[d] if BlackTarProduced[d] > 0 else float('inf')
    max_bounds.append(int(min(bound_mint, bound_active, bound_tar)))

# Brute force over feasible integer combinations
for d0 in range(max_bounds[0] + 1):
    for d1 in range(max_bounds[1] + 1):
        demos = [d0, d1]

        mint_used = sum(MintUsed[d] * demos[d] for d in range(NumDemonstrations))
        active_used = sum(ActiveIngredientUsed[d] * demos[d] for d in range(NumDemonstrations))
        tar_produced = sum(BlackTarProduced[d] * demos[d] for d in range(NumDemonstrations))

        if (mint_used <= TotalMintAvailable and
            active_used <= TotalActiveIngredientAvailable and
            tar_produced <= MaxBlackTarAllowed):

            foam = sum(FoamProduced[d] * demos[d] for d in range(NumDemonstrations))

            if foam > best_objective:
                best_objective = foam
                best_solution = demos.copy()

# Output result
if best_solution is not None:
    with open("output_solution.txt", "w") as f:
        f.write(str(best_objective))
else:
    with open("output_solution.txt", "w") as f:
        f.write("Infeasible")