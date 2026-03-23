
import os
import numpy as np
import json 
from gurobipy import Model, GRB, quicksum


model = Model("OptimizationProblem")

with open("data.json", "r") as f:
    data = json.load(f)




### Define the parameters

TotalShifts = data["TotalShifts"] # shape: [], definition: Total number of shifts available per month

TotalEnergy = data["TotalEnergy"] # shape: [], definition: Total units of energy available per month

MinOrders = data["MinOrders"] # shape: [], definition: Minimum number of orders to deliver

MinShiftsScooter = data["MinShiftsScooter"] # shape: [], definition: Minimum number of shifts on a scooter

OrdersPerBikeShift = data["OrdersPerBikeShift"] # shape: [], definition: Number of orders delivered per bike shift

EnergyPerBikeShift = data["EnergyPerBikeShift"] # shape: [], definition: Units of energy consumed per bike shift

TipsPerBikeShift = data["TipsPerBikeShift"] # shape: [], definition: Tips received per bike shift

OrdersPerScooterShift = data["OrdersPerScooterShift"] # shape: [], definition: Number of orders delivered per scooter shift

EnergyPerScooterShift = data["EnergyPerScooterShift"] # shape: [], definition: Units of energy consumed per scooter shift

TipsPerScooterShift = data["TipsPerScooterShift"] # shape: [], definition: Tips received per scooter shift



### Define the variables

BikeShifts = model.addVar(vtype=GRB.INTEGER, name="BikeShifts")

ScooterShifts = model.addVar(vtype=GRB.INTEGER, name="ScooterShifts")



### Define the constraints

model.addConstr(BikeShifts + ScooterShifts <= TotalShifts)
model.addConstr(EnergyPerBikeShift * BikeShifts + EnergyPerScooterShift * ScooterShifts <= TotalEnergy)
model.addConstr(
    OrdersPerBikeShift * BikeShifts + OrdersPerScooterShift * ScooterShifts >= MinOrders
)
model.addConstr(ScooterShifts >= MinShiftsScooter)
model.addConstr(BikeShifts >= 0)



### Define the objective

model.setObjective(
    TipsPerBikeShift * BikeShifts + TipsPerScooterShift * ScooterShifts,
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
