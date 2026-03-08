
import os
import numpy as np
import json 
from gurobipy import Model, GRB, quicksum


model = Model("OptimizationProblem")

with open("data.json", "r") as f:
    data = json.load(f)




### Define the parameters

TotalLand = data["TotalLand"] # shape: [], definition: Total land available for cultivation

WateringTimeTurnips = data["WateringTimeTurnips"] # shape: [], definition: Watering time required per acre of turnips

PesticideCostTurnips = data["PesticideCostTurnips"] # shape: [], definition: Pesticide cost per acre of turnips

WateringTimePumpkins = data["WateringTimePumpkins"] # shape: [], definition: Watering time required per acre of pumpkins

PesticideCostPumpkins = data["PesticideCostPumpkins"] # shape: [], definition: Pesticide cost per acre of pumpkins

TotalWateringTime = data["TotalWateringTime"] # shape: [], definition: Total available watering time

TotalPesticideBudget = data["TotalPesticideBudget"] # shape: [], definition: Total pesticide budget

RevenueTurnips = data["RevenueTurnips"] # shape: [], definition: Revenue per acre of turnips

RevenuePumpkins = data["RevenuePumpkins"] # shape: [], definition: Revenue per acre of pumpkins



### Define the variables

TurnipsAcres = model.addVar(vtype=GRB.CONTINUOUS, name="TurnipsAcres")

PumpkinsAcres = model.addVar(vtype=GRB.CONTINUOUS, name="PumpkinsAcres")



### Define the constraints

model.addConstr(TurnipsAcres + PumpkinsAcres <= TotalLand)
model.addConstr(WateringTimeTurnips * TurnipsAcres + WateringTimePumpkins * PumpkinsAcres <= TotalWateringTime)
model.addConstr(PesticideCostTurnips * TurnipsAcres + PesticideCostPumpkins * PumpkinsAcres <= TotalPesticideBudget)
model.addConstr(TurnipsAcres >= 0)
model.addConstr(PumpkinsAcres >= 0)


### Define the objective

model.setObjective(RevenueTurnips * TurnipsAcres + RevenuePumpkins * PumpkinsAcres, GRB.MAXIMIZE)


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
