import os
import numpy as np
import json
from gurobipy import Model, GRB, quicksum

model = Model("OptimizationProblem")

with open("data.json", "r") as f:
    data = json.load(f)

### Define the parameters

SmallPacketCapacity = data["SmallPacketCapacity"]
JugCapacity = data["JugCapacity"]
MinJugRatio = data["MinJugRatio"]
MinSmallPackets = data["MinSmallPackets"]
TotalJam = data["TotalJam"]

### Define the variables

SmallPacketSets = model.addVar(vtype=GRB.INTEGER, name="SmallPacketSets")
Jugs = model.addVar(vtype=GRB.INTEGER, name="Jugs")

### Define the constraints

model.addConstr(SmallPacketCapacity * SmallPacketSets + JugCapacity * Jugs <= TotalJam, name="JamCapacity")
model.addConstr(Jugs >= MinJugRatio * SmallPacketSets, name="JugRatio")
model.addConstr(SmallPacketSets >= MinSmallPackets, name="MinSmallPackets")
model.addConstr(SmallPacketSets >= 0, name="NonNegSmallPackets")
model.addConstr(Jugs >= 0, name="NonNegJugs")

### Define the objective (maximize total number of units sold)

model.setObjective(SmallPacketSets + Jugs, GRB.MAXIMIZE)

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