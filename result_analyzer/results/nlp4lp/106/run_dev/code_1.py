import pulp

# Create the model
model = pulp.LpProblem("OptimizationProblem", pulp.LpMinimize)

# Parameters
NumFactories = 2
NumProducts = 2

ProductionRate = [
    [12, 15],  # Factory 1: [Acne, Anti-bacterial]
    [20, 10]   # Factory 2: [Acne, Anti-bacterial]
]

BaseGelRequirement = [30, 45]
AvailableBaseGel = 5000
MinimumDemand = [800, 1000]  # [Acne, Anti-bacterial]

# Decision variables
HoursRun = [
    pulp.LpVariable(f"HoursRun_{i}", lowBound=0, cat="Continuous")
    for i in range(NumFactories)
]

# Objective: Minimize total hours run
model += pulp.lpSum(HoursRun)

# Constraint: Base gel availability
model += (
    pulp.lpSum(BaseGelRequirement[i] * HoursRun[i] for i in range(NumFactories))
    <= AvailableBaseGel
)

# Constraint: Minimum acne cream production
model += (
    pulp.lpSum(ProductionRate[f][0] * HoursRun[f] for f in range(NumFactories))
    >= MinimumDemand[0]
)

# Constraint: Minimum anti-bacterial cream production
model += (
    pulp.lpSum(ProductionRate[f][1] * HoursRun[f] for f in range(NumFactories))
    >= MinimumDemand[1]
)

# Solve the model
model.solve()

# Output optimal objective value
if pulp.LpStatus[model.status] == "Optimal":
    print("Optimal Objective Value:", pulp.value(model.objective))
    with open("output_solution.txt", "w") as f:
        f.write(str(pulp.value(model.objective)))
else:
    with open("output_solution.txt", "w") as f:
        f.write(pulp.LpStatus[model.status])