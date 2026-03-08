import os
import numpy as np
import json
from gurobipy import Model, GRB, quicksum

model = Model("OptimizationProblem")

with open("data.json", "r") as f:
    data = json.load(f)

### Define the parameters

PeoplePerSmallTruck = data["PeoplePerSmallTruck"]
PeoplePerLargeTruck = data["PeoplePerLargeTruck"]
SnowCapacitySmallTruck = data["SnowCapacitySmallTruck"]
SnowCapacityLargeTruck = data["SnowCapacityLargeTruck"]
TotalPeople = data["TotalPeople"]
MinSmallTrucks = data["MinSmallTrucks"]
MinLargeTrucks = data["MinLargeTrucks"]
SmallTrucksPerLargeTruck = data["SmallTrucksPerLargeTruck"]

### Define the variables

smallTrucks = model.addVar(vtype=GRB.INTEGER, name="smallTrucks")
largeTrucks = model.addVar(vtype=GRB.INTEGER, name="largeTrucks")

### Define the constraints

model.addConstr(PeoplePerSmallTruck * smallTrucks + 
                PeoplePerLargeTruck * largeTrucks <= TotalPeople)

model.addConstr(smallTrucks >= MinSmallTrucks)
model.addConstr(largeTrucks >= MinLargeTrucks)
model.addConstr(smallTrucks == SmallTrucksPerLargeTruck * largeTrucks)

model.addConstr(smallTrucks >= 0)
model.addConstr(largeTrucks >= 0)

### Define the objective

model.setObjective(
    SnowCapacitySmallTruck * smallTrucks +
    SnowCapacityLargeTruck * largeTrucks,
    GRB.MAXIMIZE
)

### Optimize the model

model.optimize()

### Output optimal objective value

if model.status == GRB.OPTIMAL:
    print("Optimal Objective Value:", model.ObjVal)
    with open("output_solution.txt", "w") as f:
        f.write(str(model.ObjVal))
else:
    with open("output_solution.txt", "w") as f:
        f.write(str(model.status))