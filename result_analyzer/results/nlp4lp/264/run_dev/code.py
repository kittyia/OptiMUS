
import os
import numpy as np
import json 
from gurobipy import Model, GRB, quicksum


model = Model("OptimizationProblem")

with open("data.json", "r") as f:
    data = json.load(f)




### Define the parameters

TotalAntibiotics = data["TotalAntibiotics"] # shape: [], definition: Total number of antibiotics available

AntibioticsFirstDose = data["AntibioticsFirstDose"] # shape: [], definition: Antibiotics required for one first-dose vaccine

GelatineFirstDose = data["GelatineFirstDose"] # shape: [], definition: Gelatine required for one first-dose vaccine

AntibioticsSecondDose = data["AntibioticsSecondDose"] # shape: [], definition: Antibiotics required for one second-dose vaccine

GelatineSecondDose = data["GelatineSecondDose"] # shape: [], definition: Gelatine required for one second-dose vaccine

MinimumSecondDose = data["MinimumSecondDose"] # shape: [], definition: Minimum number of second-dose vaccines required



### Define the variables

FirstDose = model.addVar(vtype=GRB.INTEGER, name="FirstDose")

SecondDose = model.addVar(vtype=GRB.INTEGER, name="SecondDose")



### Define the constraints

model.addConstr(AntibioticsFirstDose * FirstDose + AntibioticsSecondDose * SecondDose <= TotalAntibiotics)
model.addConstr(FirstDose >= SecondDose)
model.addConstr(SecondDose >= MinimumSecondDose)


### Define the objective

model.setObjective(GelatineFirstDose * FirstDose + GelatineSecondDose * SecondDose, GRB.MINIMIZE)


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
