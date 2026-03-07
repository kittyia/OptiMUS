
import os
import numpy as np
import json 
from gurobipy import Model, GRB, quicksum


model = Model("OptimizationProblem")

with open("data.json", "r") as f:
    data = json.load(f)




### Define the parameters

ProfitPerStrawberryCookie = data["ProfitPerStrawberryCookie"] # shape: [], definition: Profit per strawberry cookie

ProfitPerSugarCookie = data["ProfitPerSugarCookie"] # shape: [], definition: Profit per sugar cookie

MaxDailyDemandStrawberry = data["MaxDailyDemandStrawberry"] # shape: [], definition: Maximum daily demand for strawberry cookies

MaxDailyDemandSugar = data["MaxDailyDemandSugar"] # shape: [], definition: Maximum daily demand for sugar cookies

MaxTotalCookiesPerDay = data["MaxTotalCookiesPerDay"] # shape: [], definition: Maximum total cookies that can be made per day



### Define the variables

x2 = model.addVar(vtype=GRB.CONTINUOUS, name="x2")

x1 = model.addVar(vtype=GRB.CONTINUOUS, name="x1")



### Define the constraints

model.addConstr(x2 <= MaxDailyDemandSugar)
model.addConstr(x1 + x2 <= MaxTotalCookiesPerDay)
model.addConstr(x1 >= 0)
model.addConstr(x2 >= 0)


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
