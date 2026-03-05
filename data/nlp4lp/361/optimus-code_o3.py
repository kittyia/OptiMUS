import json
from gurobipy import Model, GRB

# ---------------------------------------------------------------------------
# 1. Load data
# ---------------------------------------------------------------------------
with open("data.json", "r") as f:
    data = json.load(f)

I       = {int(k): v for k, v in data["I"].items()}           # arrivals
F_bar   = {int(k): v for k, v in data["F_bar"].items()}       # max-flow per period
p_list  = data["p"]                                           # probability mid-points

T_index = sorted(I.keys())                                    # set of periods we have data for
avg_p   = sum(p_list) / len(p_list) if p_list else 0.0        # simple weight

# ---------------------------------------------------------------------------
# 2. Build model
# ---------------------------------------------------------------------------
model = Model("simple_multiorder_release")
model.Params.OutputFlag = 0      # silent

# Decision variables: how many orders to release in each period t
release = {}
for t in T_index:
    ub = I[t]                    # cannot release more than we currently have
    release[t] = model.addVar(vtype=GRB.INTEGER,
                              lb=0,
                              ub=ub,
                              name=f"release[{t}]")

# Maximum-flow constraints
for t in T_index:
    model.addConstr(release[t] <= F_bar[t], name=f"max_flow[{t}]")

# Objective: maximise weighted releases
model.setObjective(
    avg_p * sum(release[t] for t in T_index),
    GRB.MAXIMIZE
)

# ---------------------------------------------------------------------------
# 3. Solve
# ---------------------------------------------------------------------------
model.optimize()

# ---------------------------------------------------------------------------
# 4. Prepare solution
# ---------------------------------------------------------------------------
solution_vars = {var.VarName: var.X for var in model.getVars()}
solution = {
    "variables": solution_vars,
    "objective": model.objVal
}

with open("solution.json", "w") as f:
    json.dump(solution, f, indent=4)
