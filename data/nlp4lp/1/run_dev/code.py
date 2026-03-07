
import os
import numpy as np
import json 
from gurobipy import Model, GRB, quicksum


model = Model("OptimizationProblem")

with open("data.json", "r") as f:
    data = json.load(f)




### Define the parameters

TotalBudget = data["TotalBudget"] # shape: [], definition: Total budget available for investment

ProfitPerDollarCondos = data["ProfitPerDollarCondos"] # shape: [], definition: Profit per dollar invested in condos

ProfitPerDollarDetachedHouses = data["ProfitPerDollarDetachedHouses"] # shape: [], definition: Profit per dollar invested in detached houses

MinimumPercentageCondos = data["MinimumPercentageCondos"] # shape: [], definition: Minimum percentage of total investment that must be in condos

MinimumInvestmentDetachedHouses = data["MinimumInvestmentDetachedHouses"] # shape: [], definition: Minimum investment required in detached houses



### Define the variables

InvestmentCondos = model.addVar(vtype=GRB.CONTINUOUS, name="InvestmentCondos")

InvestmentDetachedHouses = model.addVar(vtype=GRB.CONTINUOUS, name="InvestmentDetachedHouses")



### Define the constraints

model.addConstr(InvestmentCondos + InvestmentDetachedHouses <= TotalBudget)
model.addConstr(
    InvestmentCondos >= MinimumPercentageCondos * (InvestmentCondos + InvestmentDetachedHouses)
)
model.addConstr(InvestmentDetachedHouses >= MinimumInvestmentDetachedHouses)


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
