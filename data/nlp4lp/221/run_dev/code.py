
import os
import numpy as np
import json 
from gurobipy import Model, GRB, quicksum


model = Model("OptimizationProblem")

with open("data.json", "r") as f:
    data = json.load(f)




### Define the parameters

CustomersPerThrowingGame = data["CustomersPerThrowingGame"] # shape: [], definition: Number of customers attracted per hour by throwing games

CustomersPerClimbingGame = data["CustomersPerClimbingGame"] # shape: [], definition: Number of customers attracted per hour by climbing games

PrizeCostPerThrowingGame = data["PrizeCostPerThrowingGame"] # shape: [], definition: Cost in prizes per hour for throwing games

PrizeCostPerClimbingGame = data["PrizeCostPerClimbingGame"] # shape: [], definition: Cost in prizes per hour for climbing games

MinRatioThrowingClimbing = data["MinRatioThrowingClimbing"] # shape: [], definition: Minimum ratio of throwing games to climbing games

MinClimbingGames = data["MinClimbingGames"] # shape: [], definition: Minimum number of climbing games required

MaxPrizeCostPerHour = data["MaxPrizeCostPerHour"] # shape: [], definition: Maximum total prize cost per hour



### Define the variables

ThrowingGames = model.addVar(vtype=GRB.INTEGER, name="ThrowingGames")

ClimbingGames = model.addVar(vtype=GRB.INTEGER, name="ClimbingGames")



### Define the constraints

model.addConstr(ThrowingGames >= MinRatioThrowingClimbing * ClimbingGames)
model.addConstr(ClimbingGames >= MinClimbingGames)
model.addConstr(
    PrizeCostPerThrowingGame * ThrowingGames +
    PrizeCostPerClimbingGame * ClimbingGames
    <= MaxPrizeCostPerHour
)


### Define the objective

del.setObjective(
    CustomersPerThrowingGame * ThrowingGames +
    CustomersPerClimbingGame * ClimbingGames,
    GRB.MAXIMIZE


### Optimize the model

model.optimize()



### Output optimal objective value

print("Optimal Objective Value: ", model.objVal)


if model.status == GRB.OPTIMAL:
    with open("output_solution.txt", "w") as f:
        f.write(str(model.objVal))
    print("Optimal Objective Value: ", model.objVal)
else:
    with open("output_solution.txt", "w") as f:
        f.write(model.status)
