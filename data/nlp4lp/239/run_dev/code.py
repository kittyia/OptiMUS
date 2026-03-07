
import os
import numpy as np
import json 
from gurobipy import Model, GRB, quicksum


model = Model("OptimizationProblem")

with open("data.json", "r") as f:
    data = json.load(f)




### Define the parameters

CustomersPerRetailStore = data["CustomersPerRetailStore"] # shape: [], definition: Number of customers served per retail store each day

EmployeesPerRetailStore = data["EmployeesPerRetailStore"] # shape: [], definition: Number of employees required to operate a retail store

CustomersPerFactoryOutlet = data["CustomersPerFactoryOutlet"] # shape: [], definition: Number of customers served per factory outlet each day

EmployeesPerFactoryOutlet = data["EmployeesPerFactoryOutlet"] # shape: [], definition: Number of employees required to operate a factory outlet

MinTotalCustomers = data["MinTotalCustomers"] # shape: [], definition: Minimum total number of customers required each day

MaxTotalEmployees = data["MaxTotalEmployees"] # shape: [], definition: Maximum number of employees available



### Define the variables

NumberOfRetailStores = model.addVar(vtype=GRB.INTEGER, name="NumberOfRetailStores")

NumberOfFactoryOutlets = model.addVar(vtype=GRB.INTEGER, name="NumberOfFactoryOutlets")



### Define the constraints

model.addConstr(
    CustomersPerRetailStore * NumberOfRetailStores
    + CustomersPerFactoryOutlet * NumberOfFactoryOutlets
    >= MinTotalCustomers
)
model.addConstr(EmployeesPerRetailStore * NumberOfRetailStores + EmployeesPerFactoryOutlet * NumberOfFactoryOutlets <= MaxTotalEmployees)
model.addConstr(NumberOfRetailStores >= 0)
model.addConstr(NumberOfFactoryOutlets >= 0)
model.addConstr(NumberOfRetailStores >= 0)
model.addConstr(NumberOfFactoryOutlets >= 0)


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
