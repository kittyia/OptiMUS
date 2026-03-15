import os
import json
from scipy.optimize import linprog

# Load data
with open("data.json", "r") as f:
    data = json.load(f)

# Parameters
NumSyrups = data["NumSyrups"]
MedicineThroatPerServing = data["MedicineThroatPerServing"]
MedicineLungsPerServing = data["MedicineLungsPerServing"]
SugarPerServing = data["SugarPerServing"]
MaxMedicineThroat = data["MaxMedicineThroat"]
MinMedicineLungs = data["MinMedicineLungs"]

# Objective coefficients (minimize sugar intake)
c = SugarPerServing

# Inequality constraints (A_ub x <= b_ub)
A_ub = []
b_ub = []

# Throat medicine constraint: <= MaxMedicineThroat
A_ub.append(MedicineThroatPerServing)
b_ub.append(MaxMedicineThroat)

# Lungs medicine constraint: >= MinMedicineLungs
# Convert to - (lungs) <= -MinMedicineLungs
A_ub.append([-coef for coef in MedicineLungsPerServing])
b_ub.append(-MinMedicineLungs)

# Variable bounds (non-negative servings)
bounds = [(0, None) for _ in range(NumSyrups)]

# Solve the linear program
result = linprog(c=c, A_ub=A_ub, b_ub=b_ub, bounds=bounds, method="highs")

# Output results
if result.success:
    optimal_value = result.fun
    with open("output_solution.txt", "w") as f:
        f.write(str(optimal_value))
    print("Optimal Objective Value:", optimal_value)
else:
    with open("output_solution.txt", "w") as f:
        f.write(result.message)
    print("Solver Status:", result.message)