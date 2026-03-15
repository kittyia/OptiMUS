import json
import pulp

# Create the optimization problem
model = pulp.LpProblem("OptimizationProblem", pulp.LpMinimize)

with open("data.json", "r") as f:
    data = json.load(f)

# Parameters
MinimumVitaminA = data["MinimumVitaminA"]
MinimumVitaminC = data["MinimumVitaminC"]

VitaminAPerCrabCake = data["VitaminAPerCrabCake"]
VitaminCPerCrabCake = data["VitaminCPerCrabCake"]

VitaminAPerLobsterRoll = data["VitaminAPerLobsterRoll"]
VitaminCPerLobsterRoll = data["VitaminCPerLobsterRoll"]

UnsaturatedFatPerCrabCake = data["UnsaturatedFatPerCrabCake"]
UnsaturatedFatPerLobsterRoll = data["UnsaturatedFatPerLobsterRoll"]

MaximumLobsterFraction = data["MaximumLobsterFraction"]

# Decision Variables
CrabCakes = pulp.LpVariable("CrabCakes", lowBound=0, cat=pulp.LpInteger)
LobsterRolls = pulp.LpVariable("LobsterRolls", lowBound=0, cat=pulp.LpInteger)

# Constraints
model += (
    VitaminAPerCrabCake * CrabCakes
    + VitaminAPerLobsterRoll * LobsterRolls
    >= MinimumVitaminA
)

model += (
    VitaminCPerCrabCake * CrabCakes
    + VitaminCPerLobsterRoll * LobsterRolls
    >= MinimumVitaminC
)

model += (
    LobsterRolls
    <= MaximumLobsterFraction * (CrabCakes + LobsterRolls)
)

# Objective Function
model += (
    UnsaturatedFatPerCrabCake * CrabCakes
    + UnsaturatedFatPerLobsterRoll * LobsterRolls
)

# Solve the model
model.solve()

# Output optimal objective value
if pulp.LpStatus[model.status] == "Optimal":
    with open("output_solution.txt", "w") as f:
        f.write(str(pulp.value(model.objective)))
else:
    with open("output_solution.txt", "w") as f:
        f.write(str(pulp.LpStatus[model.status]))