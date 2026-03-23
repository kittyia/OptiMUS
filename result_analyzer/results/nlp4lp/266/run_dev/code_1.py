import os  
import numpy as np  
import json  
from gurobipy import Model, GRB, quicksum  

model = Model("OptimizationProblem")  

with open("data.json", "r") as f:  
    data = json.load(f)  

### Define the parameters  

FiberSpinach = data["FiberSpinach"]  
IronSpinach = data["IronSpinach"]  
CaloriesSpinach = data["CaloriesSpinach"]  
FiberSoybeans = data["FiberSoybeans"]  
IronSoybeans = data["IronSoybeans"]  
CaloriesSoybeans = data["CaloriesSoybeans"]  
MinFiber = data["MinFiber"]  
MinIron = data["MinIron"]  

### Define the variables  

cupsSpinach = model.addVar(vtype=GRB.CONTINUOUS, name="cupsSpinach", lb=0)  
cupsSoybeans = model.addVar(vtype=GRB.CONTINUOUS, name="cupsSoybeans", lb=0)  

### Define the constraints  

model.addConstr(FiberSpinach * cupsSpinach + FiberSoybeans * cupsSoybeans >= MinFiber)  
model.addConstr(IronSpinach * cupsSpinach + IronSoybeans * cupsSoybeans >= MinIron)  
model.addConstr(cupsSpinach >= cupsSoybeans)  

### Define the objective  

model.setObjective(CaloriesSpinach * cupsSpinach + CaloriesSoybeans * cupsSoybeans, GRB.MAXIMIZE)  

### Optimize the model  

model.optimize()  

### Output optimal objective value  

if model.status == GRB.OPTIMAL:  
    print("Optimal Objective Value: ", model.ObjVal)  
    with open("output_solution.txt", "w") as f:  
        f.write(str(model.ObjVal))  
else:  
    with open("output_solution.txt", "w") as f:  
        f.write(str(model.status))