import os
import json
import itertools

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

# We assume 2 decision variables (as in the problem statement)
# x1 = servings of syrup 1
# x2 = servings of syrup 2

# Constraint equations in equality form:
# 1) Throat: a1*x1 + a2*x2 = MaxMedicineThroat
# 2) Lungs:  b1*x1 + b2*x2 = MinMedicineLungs
# 3) x1 = 0
# 4) x2 = 0

a1, a2 = MedicineThroatPerServing
b1, b2 = MedicineLungsPerServing

def solve_2x2(A, B):
    # Solve:
    # A[0][0] x1 + A[0][1] x2 = B[0]
    # A[1][0] x1 + A[1][1] x2 = B[1]
    det = A[0][0]*A[1][1] - A[0][1]*A[1][0]
    if abs(det) < 1e-9:
        return None
    x1 = (B[0]*A[1][1] - A[0][1]*B[1]) / det
    x2 = (A[0][0]*B[1] - B[0]*A[1][0]) / det
    return (x1, x2)

# Define boundary equations
equations = [
    ([[a1, a2], [b1, b2]], [MaxMedicineThroat, MinMedicineLungs]),  # throat & lungs
    ([[a1, a2], [1, 0]], [MaxMedicineThroat, 0]),                   # throat & x1=0
    ([[a1, a2], [0, 1]], [MaxMedicineThroat, 0]),                   # throat & x2=0
    ([[b1, b2], [1, 0]], [MinMedicineLungs, 0]),                    # lungs & x1=0
    ([[b1, b2], [0, 1]], [MinMedicineLungs, 0]),                    # lungs & x2=0
    ([[1, 0], [0, 1]], [0, 0])                                       # x1=0 & x2=0
]

feasible_points = []

for A, B in equations:
    sol = solve_2x2(A, B)
    if sol is None:
        continue
    x1, x2 = sol
    
    # Check feasibility:
    # Throat <= MaxMedicineThroat
    # Lungs >= MinMedicineLungs
    # x1 >= 0, x2 >= 0
    if (x1 >= -1e-9 and x2 >= -1e-9 and
        a1*x1 + a2*x2 <= MaxMedicineThroat + 1e-9 and
        b1*x1 + b2*x2 >= MinMedicineLungs - 1e-9):
        feasible_points.append((max(0, x1), max(0, x2)))

if feasible_points:
    # Minimize sugar intake
    def objective(x):
        return SugarPerServing[0]*x[0] + SugarPerServing[1]*x[1]
    
    optimal_point = min(feasible_points, key=objective)
    optimal_value = objective(optimal_point)
    
    with open("output_solution.txt", "w") as f:
        f.write(str(optimal_value))
    
    print("Optimal Objective Value:", optimal_value)
else:
    message = "No feasible solution found."
    with open("output_solution.txt", "w") as f:
        f.write(message)
    print("Solver Status:", message)