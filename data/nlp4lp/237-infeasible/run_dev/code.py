
import os
import numpy as np
import json 
from gurobipy import Model, GRB, quicksum


model = Model("OptimizationProblem")

with open("data.json", "r") as f:
    data = json.load(f)




### Define the parameters

SmallPacketCapacity = data["SmallPacketCapacity"] # shape: [], definition: Capacity of one set of small packets in milliliters

JugCapacity = data["JugCapacity"] # shape: [], definition: Capacity of one jug in milliliters

MinJugRatio = data["MinJugRatio"] # shape: [], definition: Minimum ratio of jugs to sets of small packets

MinSmallPackets = data["MinSmallPackets"] # shape: [], definition: Minimum number of sets of small packets to be filled

TotalJam = data["TotalJam"] # shape: [], definition: Total available milliliters of jam



### Define the variables

SmallPacketSets = model.addVar(vtype=GRB.INTEGER, name="SmallPacketSets")

Jugs = model.addVar(vtype=GRB.INTEGER, name="Jugs")



### Define the constraints

model.addConstr(SmallPacketCapacity * SmallPacketSets + JugCapacity * Jugs <= TotalJam)
model.addConstr(Jugs >= MinJugRatio * SmallPacketSets)
model.addConstr(SmallPacketSets >= MinSmallPackets)
model.addConstr(SmallPacketSets >= 0)
model.addConstr(Jugs >= 0)


### Define the objective




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
