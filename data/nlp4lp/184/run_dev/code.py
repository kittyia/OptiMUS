
import os
import numpy as np
import json 
from gurobipy import Model, GRB, quicksum


model = Model("OptimizationProblem")

with open("data.json", "r") as f:
    data = json.load(f)




### Define the parameters

PeoplePerSmallTruck = data["PeoplePerSmallTruck"] # shape: [], definition: Number of people required to shovel snow per small truck

PeoplePerLargeTruck = data["PeoplePerLargeTruck"] # shape: [], definition: Number of people required to shovel snow per large truck

SnowCapacitySmallTruck = data["SnowCapacitySmallTruck"] # shape: [], definition: Snow carrying capacity of a small truck (in units)

SnowCapacityLargeTruck = data["SnowCapacityLargeTruck"] # shape: [], definition: Snow carrying capacity of a large truck (in units)

TotalPeople = data["TotalPeople"] # shape: [], definition: Total number of people available for snow shoveling

MinSmallTrucks = data["MinSmallTrucks"] # shape: [], definition: Minimum number of small trucks required

MinLargeTrucks = data["MinLargeTrucks"] # shape: [], definition: Minimum number of large trucks required

SmallTrucksPerLargeTruck = data["SmallTrucksPerLargeTruck"] # shape: [], definition: Number of small trucks per large truck



### Define the variables

SmallTrucks = model.addVar(vtype=GRB.INTEGER, name="SmallTrucks")

LargeTrucks = model.addVar(vtype=GRB.INTEGER, name="LargeTrucks")



### Define the constraints

model.addConstr(PeoplePerSmallTruck * SmallTrucks + PeoplePerLargeTruck * LargeTrucks <= TotalPeople)
model.addConstr(SmallTrucks >= MinSmallTrucks)
model.addConstr(LargeTrucks >= MinLargeTrucks)
model.addConstr(SmallTrucks == SmallTrucksPerLargeTruck * LargeTrucks)
model.addConstr(SmallTrucks >= 0)
model.addConstr(LargeTrucks >= 0)


### Define the objective

model.setObjective(
    SnowCapacitySmallTruck * SmallTrucks +
    SnowCapacityLargeTruck * LargeTrucks,
    GRB.MAXIMIZE
)


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
