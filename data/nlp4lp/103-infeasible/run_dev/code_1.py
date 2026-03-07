ython
import json
import pulp

# Create the optimization model (Minimization)
model = pulp.LpProblem("OptimizationProblem", pulp.LpMinimize)

# Load data
with open("data.json", "r") as f:
    data = json.load(f)

# Parameters
TotalMRNAAvailable = data["TotalMRNAAvailable"]
MRNAPerChildVaccine = data["MRNAPerChildVaccine"]
MRNAPerAdultVaccine = data["MRNAPerAdultVaccine"]
FeverSuppressantPerChildVaccine = data["FeverSuppressantPerChildVaccine"]
FeverSuppressantPerAdultVaccine = data["FeverSuppressantPerAdultVaccine"]
MinPercentageAdultVaccines = data["MinPercentageAdultVaccines"]
MinChildVaccines = data["MinChildVaccines"]

# Decision Variables
childVaccines = pulp.LpVariable("childVaccines", lowBound=0, cat="Integer")
adultVaccines = pulp.LpVariable("adultVaccines", lowBound=0, cat="Integer")

# Objective Function: Minimize total fever suppressant used
model += (FeverSuppressantPerChildVaccine * childVaccines +
          FeverSuppressantPerAdultVaccine * adultVaccines)

# Constraints

# mRNA availability constraint
model += (MRNAPerChildVaccine * childVaccines +
          MRNAPerAdultVaccine * adultVaccines <= TotalMRNAAvailable)

# At least the minimum percentage of vaccines must be adult vaccines
# adult >= (MinPercentageAdultVaccines/100) * (child + adult)
model += adultVaccines >= (MinPercentageAdultVaccines / 100.0) * (childVaccines + adultVaccines)

# At least minimum number of children's vaccines
model += childVaccines >= MinChildVaccines

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
``