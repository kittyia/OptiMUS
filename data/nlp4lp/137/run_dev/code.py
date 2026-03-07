
import os
import numpy as np
import json 
from gurobipy import Model, GRB, quicksum


model = Model("OptimizationProblem")

with open("data.json", "r") as f:
    data = json.load(f)




### Define the parameters

TotalPopsicleSticks = data["TotalPopsicleSticks"] # shape: [], definition: Total number of Popsicle sticks available

PopsicleSticksPerBeamBridge = data["PopsicleSticksPerBeamBridge"] # shape: [], definition: Number of Popsicle sticks required to build one beam bridge

PopsicleSticksPerTrussBridge = data["PopsicleSticksPerTrussBridge"] # shape: [], definition: Number of Popsicle sticks required to build one truss bridge

TotalGlue = data["TotalGlue"] # shape: [], definition: Total units of glue available

GluePerBeamBridge = data["GluePerBeamBridge"] # shape: [], definition: Units of glue required to build one beam bridge

GluePerTrussBridge = data["GluePerTrussBridge"] # shape: [], definition: Units of glue required to build one truss bridge

MaxTrussBridges = data["MaxTrussBridges"] # shape: [], definition: Maximum number of truss bridges that can be built

MassPerBeamBridge = data["MassPerBeamBridge"] # shape: [], definition: Mass that one beam bridge can hold

MassPerTrussBridge = data["MassPerTrussBridge"] # shape: [], definition: Mass that one truss bridge can hold



### Define the variables

BeamBridges = model.addVar(vtype=GRB.INTEGER, name="BeamBridges")

TrussBridges = model.addVar(vtype=GRB.INTEGER, name="TrussBridges")



### Define the constraints

model.addConstr(PopsicleSticksPerBeamBridge * BeamBridges + PopsicleSticksPerTrussBridge * TrussBridges <= TotalPopsicleSticks)
model.addConstr(GluePerBeamBridge * BeamBridges + GluePerTrussBridge * TrussBridges <= TotalGlue)
model.addConstr(TrussBridges <= MaxTrussBridges)
model.addConstr(BeamBridges >= TrussBridges + 1)
model.addConstr(BeamBridges >= 0)
model.addConstr(TrussBridges >= 0)


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
