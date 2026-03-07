
import os
import numpy as np
import json 
from gurobipy import Model, GRB, quicksum


model = Model("OptimizationProblem")

with open("data.json", "r") as f:
    data = json.load(f)




### Define the parameters

EmployeesPerTaxiRide = data["EmployeesPerTaxiRide"] # shape: [], definition: Number of employees that can be transported in one taxi ride.

EmployeesPerCompanyCarRide = data["EmployeesPerCompanyCarRide"] # shape: [], definition: Number of employees that can be transported in one company car ride.

MaxCompanyCarRidePercentage = data["MaxCompanyCarRidePercentage"] # shape: [], definition: The upper limit on the proportion of total rides that can be company car rides.

MinCompanyCarRides = data["MinCompanyCarRides"] # shape: [], definition: The minimum required number of company car rides.

MinEmployees = data["MinEmployees"] # shape: [], definition: The minimum number of employees that need to be transported.



### Define the variables

TaxiRides = model.addVar(vtype=GRB.INTEGER, name="TaxiRides")

CompanyCarRides = model.addVar(vtype=GRB.INTEGER, name="CompanyCarRides")



### Define the constraints

model.addConstr(
    EmployeesPerTaxiRide * TaxiRides
    + EmployeesPerCompanyCarRide * CompanyCarRides
    >= MinEmployees
)
model.addConstr(CompanyCarRides <= (MaxCompanyCarRidePercentage / 100.0) * (TaxiRides + CompanyCarRides))
model.addConstr(CompanyCarRides >= MinCompanyCarRides)
model.addConstr(TaxiRides >= 0)
model.addConstr(CompanyCarRides >= 0)


### Define the objective

model.setObjective(TaxiRides, GRB.MINIMIZE)


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
