import os
import json
import pulp

# Create the optimization problem (minimization)
model = pulp.LpProblem("OptimizationProblem", pulp.LpMinimize)

with open("data.json", "r") as f:
    data = json.load(f)

# Define the parameters
NumSyrups = data["NumSyrups"]
MedicineThroatPerServing = data["MedicineThroatPerServing"]
MedicineLungsPerServing = data["MedicineLungsPerServing"]
SugarPerServing = data["SugarPerServing"]
MaxMedicineThroat = data["MaxMedicineThroat"]
MinMedicineLungs = data["MinMedicineLungs"]

# Define the variables (continuous and non-negative)
Servings = [
    pulp.LpVariable(f"Servings_{i}", lowBound=0, cat="Continuous")
    for i in range(NumSyrups)
]

# Define the objective (minimize total sugar intake)
model += pulp.lpSum(SugarPerServing[i] * Servings[i] for i in range(NumSyrups))

# Define the constraints
model += (
    pulp.lpSum(MedicineThroatPerServing[i] * Servings[i] for i in range(NumSyrups))
    <= MaxMedicineThroat
)

model += (
    pulp.lpSum(MedicineLungsPerServing[i] * Servings[i] for i in range(NumSyrups))
    >= MinMedicineLungs
)

# Solve the model
model.solve()

# Output optimal objective value
if pulp.LpStatus[model.status] == "Optimal":
    optimal_value = pulp.value(model.objective)
    with open("output_solution.txt", "w") as f:
        f.write(str(optimal_value))
    print("Optimal Objective Value:", optimal_value)
else:
    with open("output_solution.txt", "w") as f:
        f.write(pulp.LpStatus[model.status])
    print("Solver Status:", pulp.LpStatus[model.status])