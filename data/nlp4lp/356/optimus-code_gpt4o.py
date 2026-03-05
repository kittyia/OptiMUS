import json
from gurobipy import *

# Load data
with open("data.json", "r") as f:
    data = json.load(f)

# Extract data
students = data["S"]
classes = data["C"]
enrollments = data["A"]
class_capacity = data["c"]
excess_capacity = data["E"]
num_groups = data["G"]
num_time_slots = data["T"]
lambda_weight = data["lambda"]
mu_weight = data["mu"]

# Create model
model = Model("HybridScheduling")

# Variables
pi = model.addVars(len(students), num_groups, vtype=GRB.BINARY, name="pi")
excess = model.addVars(len(classes), len(students), vtype=GRB.BINARY, name="excess")

# Objective: Minimize weighted sum of total excess (TE), total deviation (TD), and surplus simultaneous excess (SSE)
TE = quicksum(excess[c, s] for c in range(len(classes)) for s in range(len(students)))
TD = quicksum((pi[s, g] - 1/num_groups) * (pi[s, g] - 1/num_groups) for s in range(len(students)) for g in range(num_groups))
SSE = quicksum(excess[c, s] for c in range(len(classes)) for s in range(len(students)))

model.setObjective(TE + lambda_weight * TD + mu_weight * SSE, GRB.MINIMIZE)

# Constraints
# Each student should be assigned to exactly one group
for s in range(len(students)):
    model.addConstr(quicksum(pi[s, g] for g in range(num_groups)) == 1)

# For each class, ensure social distancing capacity is not exceeded
for c, class_name in enumerate(classes):
    enrolled_students = enrollments[class_name]
    for s, student in enumerate(students):
        if student in enrolled_students:
            model.addConstr(quicksum(pi[students.index(student), g] for g in range(num_groups)) <= class_capacity[class_name] + excess[c, s])

# Excess room capacity constraint
for c in range(len(classes)):
    model.addConstr(quicksum(excess[c, s] for s in range(len(students))) <= excess_capacity)

# Optimize model
model.optimize()

# Write solution to solution.json
solution = {
    "variables": {
        "pi": [[pi[s, g].x for g in range(num_groups)] for s in range(len(students))],
        "excess": [[excess[c, s].x for s in range(len(students))] for c in range(len(classes))]
    },
    "objective": model.objVal
}

with open("solution.json", "w") as f:
    json.dump(solution, f, indent=4)
