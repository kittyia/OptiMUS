import json
from pulp import LpProblem, LpVariable, LpMinimize, LpStatus, value

# Load data
with open("data.json", "r") as f:
    data = json.load(f)

# Parameters
TimePerFertilizer = data["TimePerFertilizer"]
TimePerSeeds = data["TimePerSeeds"]
MaxTotalUnits = data["MaxTotalUnits"]
MinFertilizer = data["MinFertilizer"]
MaxFertilizerRatio = data["MaxFertilizerRatio"]

# Create model
model = LpProblem("OptimizationProblem", LpMinimize)

# Decision variables
FertilizerUnits = LpVariable("FertilizerUnits", lowBound=0, cat="Continuous")
SeedsUnits = LpVariable("SeedsUnits", lowBound=0, cat="Continuous")

# Constraints
model += FertilizerUnits + SeedsUnits <= MaxTotalUnits
model += FertilizerUnits >= MinFertilizer
model += FertilizerUnits <= MaxFertilizerRatio * SeedsUnits

# Objective function
model += TimePerFertilizer * FertilizerUnits + TimePerSeeds * SeedsUnits

# Solve
model.solve()

# Output results
if LpStatus[model.status] == "Optimal":
    optimal_value = value(model.objective)
    with open("output_solution.txt", "w") as f:
        f.write(str(optimal_value))
    print("Optimal Objective Value:", optimal_value)
else:
    with open("output_solution.txt", "w") as f:
        f.write(LpStatus[model.status])
    print("Solver Status:", LpStatus[model.status])