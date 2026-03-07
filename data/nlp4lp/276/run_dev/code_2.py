import json
from gurobipy import Model, GRB, quicksum

model = Model("OptimizationProblem")

with open("data.json", "r") as f:
    data = json.load(f)

# Define the parameters
InitialPosition = data["InitialPosition"]
InitialVelocity = data["InitialVelocity"]
FinalPosition = data["FinalPosition"]
FinalVelocity = data["FinalVelocity"]
TotalTime = data["TotalTime"]

# Define the variables
Position = model.addVars(TotalTime + 1, vtype=GRB.CONTINUOUS, name="Position")
Velocity = model.addVars(TotalTime + 1, vtype=GRB.CONTINUOUS, name="Velocity")
Acceleration = model.addVars(TotalTime, vtype=GRB.CONTINUOUS, name="Acceleration")

# Auxiliary variables to model |Acceleration[t]|
Fuel = model.addVars(TotalTime, vtype=GRB.CONTINUOUS, lb=0.0, name="Fuel")

# Define the constraints
for t in range(TotalTime):
    model.addConstr(Position[t+1] == Position[t] + Velocity[t])

for t in range(TotalTime):
    model.addConstr(Velocity[t+1] == Velocity[t] + Acceleration[t])

# Absolute value linearization constraints
for t in range(TotalTime):
    model.addConstr(Fuel[t] >= Acceleration[t])
    model.addConstr(Fuel[t] >= -Acceleration[t])

model.addConstr(Position[0] == InitialPosition)
model.addConstr(Velocity[0] == InitialVelocity)
model.addConstr(Position[TotalTime] == FinalPosition)
model.addConstr(Velocity[TotalTime] == FinalVelocity)

# Define the objective
model.setObjective(quicksum(Fuel[t] for t in range(TotalTime)), GRB.MINIMIZE)

# Optimize the model
model.optimize()

# Output optimal objective value
if model.status == GRB.OPTIMAL:
    print("Optimal Objective Value: ", model.objVal)
    with open("output_solution.txt", "w") as f:
        f.write(str(model.objVal))
else:
    with open("output_solution.txt", "w") as f:
        f.write(str(model.status))