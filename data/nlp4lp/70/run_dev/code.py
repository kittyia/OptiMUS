
import os
import numpy as np
import json 
from gurobipy import Model, GRB, quicksum


model = Model("OptimizationProblem")

with open("data.json", "r") as f:
    data = json.load(f)




### Define the parameters

NumFireFighterTypes = data["NumFireFighterTypes"] # shape: [], definition: Number of fire fighter types

HoursPerShift = data["HoursPerShift"] # shape: ['NumFireFighterTypes'], definition: Amount of hours each fire fighter type works per shift

CostPerShift = data["CostPerShift"] # shape: ['NumFireFighterTypes'], definition: Cost of each fire fighter type per shift

TotalHoursRequired = data["TotalHoursRequired"] # shape: [], definition: Total required fire fighter hours

Budget = data["Budget"] # shape: [], definition: Total available budget



### Define the variables

FireFightersHired = model.addVars(NumFireFighterTypes, vtype=GRB.INTEGER, name="FireFightersHired")



### Define the constraints

model.addConstr(
    sum(HoursPerShift[t] * FireFightersHired[t] for t in range(NumFireFighterTypes)) 
    >= TotalHoursRequired
)
model.addConstr(
    sum(CostPerShift[i] * FireFightersHired[i] for i in range(NumFireFighterTypes)) 
    <= Budget
)
for i in range(NumFireFighterTypes):
    model.addConstr(FireFightersHired[i] >= 0)
for i in range(NumFireFighterTypes):
    model.addConstr(FireFightersHired[i] >= 0)


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
