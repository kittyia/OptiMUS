
import os
import numpy as np
import json 
from gurobipy import Model, GRB, quicksum


model = Model("OptimizationProblem")

with open("data.json", "r") as f:
    data = json.load(f)




### Define the parameters

HoursSeasonal = data["HoursSeasonal"] # shape: [], definition: Number of hours per shift for a seasonal snow remover

PaymentSeasonal = data["PaymentSeasonal"] # shape: [], definition: Payment per shift for a seasonal snow remover

HoursPermanent = data["HoursPermanent"] # shape: [], definition: Number of hours per shift for a permanent snow remover

PaymentPermanent = data["PaymentPermanent"] # shape: [], definition: Payment per shift for a permanent snow remover

RequiredLaborHours = data["RequiredLaborHours"] # shape: [], definition: Total required labor hours after a heavy snowfall

TotalBudget = data["TotalBudget"] # shape: [], definition: Total budget available for hiring snow removers



### Define the variables

SeasonalWorkers = model.addVar(vtype=GRB.INTEGER, name="SeasonalWorkers")

PermanentWorkers = model.addVar(vtype=GRB.INTEGER, name="PermanentWorkers")



### Define the constraints

model.addConstr(HoursSeasonal * SeasonalWorkers + HoursPermanent * PermanentWorkers >= RequiredLaborHours)
model.addConstr(PaymentSeasonal * SeasonalWorkers + PaymentPermanent * PermanentWorkers <= TotalBudget)
model.addConstr(SeasonalWorkers >= 0)
model.addConstr(PermanentWorkers >= 0)


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
