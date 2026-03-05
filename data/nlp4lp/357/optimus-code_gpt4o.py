import json
from gurobipy import *

# Load data
with open("data.json", "r") as f:
    data = json.load(f)

# Extract data
students = data["S"]
classes = data["C"]
enrollments = data["A"]
capacities = data["c"]
class_times = data["C_t"]
lambda_weight = data["lambda"]
mu_weight = data["mu"]
num_hours = data["T"]

# Create model
model = Model("HybridScheduling")

# Decision variables
x = model.addVars(students, classes, vtype=GRB.BINARY, name="x")
y = model.addVars(classes, num_hours, vtype=GRB.BINARY, name="y")

# Objective: Maximize interaction
TE = quicksum((x[s, c] - y[c, t]) for c in classes for t in range(num_hours) for s in enrollments[c] if c in class_times[str(t)])
TD = quicksum((x[s, c] - y[c, t]) for c in classes for t in range(num_hours) for s in enrollments[c] if c in class_times[str(t)])
SSE = quicksum((x[s, c] - y[c, t]) for c in classes for t in range(num_hours) for s in enrollments[c] if c in class_times[str(t)])

model.setObjective(TE + lambda_weight * TD + mu_weight * SSE, GRB.MAXIMIZE)

# Constraints
# 1. Exactly four learning teams attending classes in person on each day
for t in range(num_hours):
    model.addConstr(quicksum(y[c, t] for c in class_times[str(t)]) == 4, name=f"FourTeams_{t}")

# 2. Longitudinal balance being maintained
# (Assuming longitudinal balance means equal distribution over the term)
for s in students:
    model.addConstr(quicksum(x[s, c] for c in classes) == num_hours // len(classes), name=f"LongitudinalBalance_{s}")

# 3. Balance over days of the week being maintained
# (Assuming balance over days of the week means equal distribution over the week)
for s in students:
    for day in range(7):
        model.addConstr(quicksum(x[s, c] for c in classes if c in class_times[str(day)]) == num_hours // 7, name=f"WeeklyBalance_{s}_{day}")

# 4. Social distancing capacity constraint
for c in classes:
    for t in range(num_hours):
        model.addConstr(quicksum(x[s, c] for s in enrollments[c]) <= capacities[c], name=f"Capacity_{c}_{t}")

# Optimize model
model.optimize()

# Write solution
solution = {
    "variables": {f"x[{s},{c}]": x[s, c].X for s in students for c in classes},
    "objective": model.objVal
}

with open("solution.json", "w") as f:
    json.dump(solution, f, indent=4)
