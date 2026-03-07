
import os
import numpy as np
import json 
from gurobipy import Model, GRB, quicksum


model = Model("OptimizationProblem")

with open("data.json", "r") as f:
    data = json.load(f)




### Define the parameters

PreventionPillCost = data["PreventionPillCost"] # shape: [], definition: Cost to make one prevention pill

TreatmentPillCost = data["TreatmentPillCost"] # shape: [], definition: Cost to make one treatment pill

PreventionToTreatmentRatio = data["PreventionToTreatmentRatio"] # shape: [], definition: Minimum ratio of prevention pills to treatment pills

MinimumTreatmentPills = data["MinimumTreatmentPills"] # shape: [], definition: Minimum number of treatment pills to purchase

Budget = data["Budget"] # shape: [], definition: Total budget available for purchasing pills



### Define the variables

PreventionPills = model.addVar(vtype=GRB.INTEGER, name="PreventionPills")

TreatmentPills = model.addVar(vtype=GRB.INTEGER, name="TreatmentPills")



### Define the constraints

model.addConstr(PreventionPills >= PreventionToTreatmentRatio * TreatmentPills)
model.addConstr(TreatmentPills >= MinimumTreatmentPills)
model.addConstr(PreventionPillCost * PreventionPills + TreatmentPillCost * TreatmentPills <= Budget)


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
