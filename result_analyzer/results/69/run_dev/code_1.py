import json
from gurobipy import Model, GRB

model = Model("OptimizationProblem")

with open("data.json", "r") as f:
    data = json.load(f)

### Define the parameters

ChocolateSpreadPerChocolateCrepe = data["ChocolateSpreadPerChocolateCrepe"]
PeanutButterSpreadPerPeanutButterCrepe = data["PeanutButterSpreadPerPeanutButterCrepe"]
CrepeMixPerChocolateCrepe = data["CrepeMixPerChocolateCrepe"]
CrepeMixPerPeanutButterCrepe = data["CrepeMixPerPeanutButterCrepe"]
TotalAvailableChocolateSpread = data["TotalAvailableChocolateSpread"]
TotalAvailablePeanutButterSpread = data["TotalAvailablePeanutButterSpread"]
MinimumProportionChocolateCrepes = data["MinimumProportionChocolateCrepes"]

### Define the variables

ChocolateCrepes = model.addVar(vtype=GRB.INTEGER, name="ChocolateCrepes", lb=0)
PeanutButterCrepes = model.addVar(vtype=GRB.INTEGER, name="PeanutButterCrepes", lb=0)

### Define the constraints

model.addConstr(
    ChocolateSpreadPerChocolateCrepe * ChocolateCrepes
    <= TotalAvailableChocolateSpread
)

model.addConstr(
    PeanutButterSpreadPerPeanutButterCrepe * PeanutButterCrepes
    <= TotalAvailablePeanutButterSpread
)

model.addConstr(PeanutButterCrepes >= ChocolateCrepes)

model.addConstr(
    ChocolateCrepes
    >= MinimumProportionChocolateCrepes * (ChocolateCrepes + PeanutButterCrepes)
)

### Define the objective

model.setObjective(
    CrepeMixPerChocolateCrepe * ChocolateCrepes
    + CrepeMixPerPeanutButterCrepe * PeanutButterCrepes,
    GRB.MINIMIZE
)

### Optimize the model

model.optimize()

### Output optimal objective value

if model.status == GRB.OPTIMAL:
    print("Optimal Objective Value: ", model.objVal)
    with open("output_solution.txt", "w") as f:
        f.write(str(model.objVal))
else:
    with open("output_solution.txt", "w") as f:
        f.write(str(model.status))