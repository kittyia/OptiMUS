
import os
import numpy as np
import json 
from gurobipy import Model, GRB, quicksum


model = Model("OptimizationProblem")

with open("data.json", "r") as f:
    data = json.load(f)




### Define the parameters

TimeElectronicReading = data["TimeElectronicReading"] # shape: [], definition: Time taken by electronic thermometer per reading

TimeRegularReading = data["TimeRegularReading"] # shape: [], definition: Time taken by regular thermometer per reading

MinRatioElectronicToRegular = data["MinRatioElectronicToRegular"] # shape: [], definition: Minimum ratio of electronic thermometer uses to regular thermometer uses

MinRegularPatients = data["MinRegularPatients"] # shape: [], definition: Minimum number of patients using regular thermometer

TotalAvailableTime = data["TotalAvailableTime"] # shape: [], definition: Total available time for temperature readings



### Define the variables

NumberElectronicPatients = model.addVar(vtype=GRB.INTEGER, name="NumberElectronicPatients")

NumberRegularPatients = model.addVar(vtype=GRB.INTEGER, name="NumberRegularPatients")



### Define the constraints

model.addConstr(TimeElectronicReading * NumberElectronicPatients + TimeRegularReading * NumberRegularPatients <= TotalAvailableTime)
model.addConstr(NumberElectronicPatients >= MinRatioElectronicToRegular * NumberRegularPatients)
model.addConstr(NumberRegularPatients >= MinRegularPatients)


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
