import os
import numpy as np
import json 
from gurobipy import Model, GRB, quicksum


model = Model("OptimizationProblem")

with open("data.json", "r") as f:
    data = json.load(f)


### Define the parameters

TransportCapacity = data["TransportCapacity"]
TransportCost = data["TransportCost"]
MinimumHydrogen = data["MinimumHydrogen"]
Budget = data["Budget"]
NumTransportMethods = data["NumTransportMethods"]


### Define the variables

HighPressureTrips = model.addVar(vtype=GRB.INTEGER, lb=0, name="HighPressureTrips")
LiquefiedTrips = model.addVar(vtype=GRB.INTEGER, lb=0, name="LiquefiedTrips")


### Define the constraints

model.addConstr(50 * HighPressureTrips + 30 * LiquefiedTrips >= MinimumHydrogen, name="HydrogenRequirement")
model.addConstr(500 * HighPressureTrips + 200 * LiquefiedTrips <= Budget, name="BudgetConstraint")
model.addConstr(HighPressureTrips <= LiquefiedTrips - 1, name="TripRelation")


### Define the objective (minimize total number of trips)

model.setObjective(HighPressureTrips + LiquefiedTrips, GRB.MINIMIZE)


### Optimize the model

model.optimize()


### Output optimal objective value

if model.status == GRB.OPTIMAL:
    print("Optimal Objective Value: ", model.ObjVal)
    with open("output_solution.txt", "w") as f:
        f.write(str(model.ObjVal))
else:
    with open("output_solution.txt", "w") as f:
        f.write(str(model.status))