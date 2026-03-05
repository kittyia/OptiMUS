import json
from gurobipy import *

# 1. -------------------------------------------------------------------------
#    Load data
with open("data.json", "r") as f:
    data = json.load(f)

students = data["S"]                          # list of student ids
G         = data["G"]                         # number of groups (integer)

# 2. -------------------------------------------------------------------------
#    Build model
model = Model("hybrid_group_assignment")

# Decision variables: pi[i,j] = 1 if student i assigned to group j
pi = {}
for i, stu in enumerate(students):
    for j in range(G):
        var_name      = f"pi_{stu}_{j}"
        pi[stu, j]    = model.addVar(vtype=GRB.BINARY, name=var_name)

# Each student assigned to exactly one group
for stu in students:
    model.addConstr(quicksum(pi[stu, j] for j in range(G)) == 1,
                    name=f"assign_{stu}")

# Objective (placeholder):
# Minimise weighted group number each student is assigned to
model.setObjective(quicksum(j * pi[stu, j] for stu in students for j in range(G)),
                   GRB.MINIMIZE)

# 3. -------------------------------------------------------------------------
#    Optimise
model.optimize()

# 4. -------------------------------------------------------------------------
#    Write solution
solution_vars = {var.VarName: int(round(var.X)) for var in model.getVars()}

solution = {
    "variables": solution_vars,
    "objective": model.objVal
}

with open("solution.json", "w") as f:
    json.dump(solution, f, indent=4)
