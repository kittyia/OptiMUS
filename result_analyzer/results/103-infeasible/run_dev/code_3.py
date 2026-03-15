import json
import numpy as np
from scipy.optimize import linprog

# Load data
with open("data.json", "r") as f:
    data = json.load(f)

# Parameters
TotalMRNAAvailable = data["TotalMRNAAvailable"]
MRNAPerChildVaccine = data["MRNAPerChildVaccine"]
MRNAPerAdultVaccine = data["MRNAPerAdultVaccine"]
FeverSuppressantPerChildVaccine = data["FeverSuppressantPerChildVaccine"]
FeverSuppressantPerAdultVaccine = data["FeverSuppressantPerAdultVaccine"]
MinPercentageAdultVaccines = data["MinPercentageAdultVaccines"] / 100.0
MinChildVaccines = data["MinChildVaccines"]

# Objective function coefficients (minimize fever suppressant)
c = [
    FeverSuppressantPerChildVaccine,   # child vaccines
    FeverSuppressantPerAdultVaccine    # adult vaccines
]

# Inequality constraints (A_ub x <= b_ub)

A_ub = []
b_ub = []

# 1. mRNA availability constraint
A_ub.append([MRNAPerChildVaccine, MRNAPerAdultVaccine])
b_ub.append(TotalMRNAAvailable)

# 2. Adult percentage constraint:
# adult >= p * (child + adult)
# => adult - p*child - p*adult >= 0
# => p*child - (1-p)*adult <= 0
A_ub.append([MinPercentageAdultVaccines, -(1 - MinPercentageAdultVaccines)])
b_ub.append(0)

# 3. Minimum children constraint:
# child >= MinChildVaccines
# => -child <= -MinChildVaccines
A_ub.append([-1, 0])
b_ub.append(-MinChildVaccines)

# Variable bounds: child >= 0, adult >= 0
bounds = [(0, None), (0, None)]

# Solve using linear programming
result = linprog(c, A_ub=A_ub, b_ub=b_ub, bounds=bounds, method="highs")

# Output results
if result.success:
    optimal_value = result.fun
    print("Optimal Objective Value:", optimal_value)
    with open("output_solution.txt", "w") as f:
        f.write(str(optimal_value))
else:
    with open("output_solution.txt", "w") as f:
        f.write("Infeasible")