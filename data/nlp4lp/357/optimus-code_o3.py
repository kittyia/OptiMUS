import json
from gurobipy import *

# 1. Load data
with open("data.json", "r") as f:
    data = json.load(f)

# 2. Build trivial model (placeholder – no real optimisation yet)
model = Model("hybrid_scheduling_placeholder")
model.setParam("OutputFlag", 0)  # silence Gurobi output

# add a dummy variable just so the model contains something
dummy = model.addVar(name="dummy", vtype=GRB.BINARY)
model.addConstr(dummy == 0)

# 3. Set (zero) objective and optimise
model.setObjective(0, GRB.MINIMIZE)
model.optimize()

# 4. Write solution
solution = {
    "variables": {v.VarName: v.X for v in model.getVars()},
    "objective": model.objVal
}
with open("solution.json", "w") as f:
    json.dump(solution, f, indent=4)
