
import os
import numpy as np
import json 
from gurobipy import Model, GRB, quicksum


model = Model("OptimizationProblem")

with open("data.json", "r") as f:
    data = json.load(f)




### Define the parameters

Demand = data["Demand"] # shape: ['NumMonths'], definition: Demand of product n

MaxRegularAmount = data["MaxRegularAmount"] # shape: [], definition: Maximum production amount under regular conditions

CostRegular = data["CostRegular"] # shape: [], definition: Cost of production under regular conditions per unit

CostOvertime = data["CostOvertime"] # shape: [], definition: Cost of production under overtime conditions per unit

StoreCost = data["StoreCost"] # shape: [], definition: Cost to store one unit of product

NumMonths = data["NumMonths"] # shape: [], definition: Number of months in the planning horizon



### Define the variables

regQuant = model.addVars(NumMonths, vtype=GRB.CONTINUOUS, name="regQuant")

overQuant = model.addVars(NumMonths, vtype=GRB.CONTINUOUS, name="overQuant")

inventory = model.addVars(NumMonths, vtype=GRB.CONTINUOUS, name="inventory")



### Define the constraints

for n in range(NumMonths):
    model.addConstr(regQuant[n] >= 0)
    model.addConstr(regQuant[n] <= MaxRegularAmount)
for n in range(NumMonths):
    if n == 0:
        model.addConstr(regQuant[n] + overQuant[n] == Demand[n] + inventory[n])
    else:
        model.addConstr(inventory[n-1] + regQuant[n] + overQuant[n] == Demand[n] + inventory[n])
for n in range(NumMonths):
    model.addConstr(inventory[n] >= 0)
for n in range(NumMonths):
    model.addConstr(overQuant[n] >= 0)
model.addConstr(inventory[0] == 0)


### Define the objective

model.setObjective(
    quicksum(
        CostRegular * regQuant[n] +
        CostOvertime * overQuant[n] +
        StoreCost * inventory[n]
        for n in range(NumMonths)
    ),
    GRB.MINIMIZE
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
