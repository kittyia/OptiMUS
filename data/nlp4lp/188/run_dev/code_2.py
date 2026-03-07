import os
import numpy as np
import json
from gurobipy import Model, GRB, quicksum

model = Model("OptimizationProblem")

with open("data.json", "r") as f:
    data = json.load(f)

# Define the parameters
VoterCapacityVan = data["VoterCapacityVan"]  # Number of voters a van can carry
VoterCapacityCar = data["VoterCapacityCar"]  # Number of voters a car can carry
MinVoters = data["MinVoters"]  # Minimum number of voters to transport
MaxVanPercentage = data["MaxVanPercentage"]  # Maximum percentage of vehicles that can be vans

# Define the variables
NumberOfVans = model.addVar(vtype=GRB.INTEGER, lb=0, name="NumberOfVans")
NumberOfCars = model.addVar(vtype=GRB.INTEGER, lb=0, name="NumberOfCars")

# Define the constraints

# Capacity constraint
model.addConstr(
    VoterCapacityVan * NumberOfVans + VoterCapacityCar * NumberOfCars >= MinVoters
)

# At most 30% of vehicles can be vans:
# NumberOfVans <= 0.3 * (NumberOfVans + NumberOfCars)
# Rearranged: 7 * NumberOfVans <= 3 * NumberOfCars
model.addConstr(7 * NumberOfVans <= 3 * NumberOfCars)

# Define the objective
model.setObjective(NumberOfCars, GRB.MINIMIZE)

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