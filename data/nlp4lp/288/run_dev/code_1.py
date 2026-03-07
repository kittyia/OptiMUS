import os
import numpy as np
import json
from gurobipy import Model, GRB, quicksum


model = Model("OptimizationProblem")

with open("data.json", "r") as f:
    data = json.load(f)


# Define the parameters
TotalHectares = data["TotalHectares"]
MinTomatoes = data["MinTomatoes"]
MinPotatoes = data["MinPotatoes"]
MaxTomatoesToPotatoesRatio = data["MaxTomatoesToPotatoesRatio"]
ProfitPerHectareTomatoes = data["ProfitPerHectareTomatoes"]
ProfitPerHectarePotatoes = data["ProfitPerHectarePotatoes"]


# Define the variables
TomatoHectares = model.addVar(vtype=GRB.CONTINUOUS, name="TomatoHectares")
PotatoHectares = model.addVar(vtype=GRB.CONTINUOUS, name="PotatoHectares")


# Define the constraints
model.addConstr(TomatoHectares + PotatoHectares <= TotalHectares)
model.addConstr(TomatoHectares <= MaxTomatoesToPotatoesRatio * PotatoHectares)
model.addConstr(TomatoHectares >= MinTomatoes)
model.addConstr(PotatoHectares >= MinPotatoes)


# Define the objective
model.setObjective(
    ProfitPerHectareTomatoes * TomatoHectares +
    ProfitPerHectarePotatoes * PotatoHectares,
    GRB.MAXIMIZE
)


# Optimize the model
model.optimize()


# Output optimal objective value
if model.status == GRB.OPTIMAL:
    print("Optimal Objective Value: ", model.ObjVal)
    with open("output_solution.txt", "w") as f:
        f.write(str(model.ObjVal))
else:
    with open("output_solution.txt", "w") as f:
        f.write(str(model.status))