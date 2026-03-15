
import os
import numpy as np
import json 
from gurobipy import Model, GRB, quicksum


model = Model("OptimizationProblem")

with open("data.json", "r") as f:
    data = json.load(f)




### Define the parameters

CostPersonalLicense = data["CostPersonalLicense"] # shape: [], definition: Cost to generate a personal license

CostCommercialLicense = data["CostCommercialLicense"] # shape: [], definition: Cost to generate a commercial license

ProfitPersonalLicense = data["ProfitPersonalLicense"] # shape: [], definition: Profit per personal license

ProfitCommercialLicense = data["ProfitCommercialLicense"] # shape: [], definition: Profit per commercial license

MaxTotalLicenses = data["MaxTotalLicenses"] # shape: [], definition: Maximum total licenses that can be sold per month

MaxTotalExpenditure = data["MaxTotalExpenditure"] # shape: [], definition: Maximum total expenditure allowed by the company



### Define the variables

PersonalLicenses = model.addVar(vtype=GRB.INTEGER, name="PersonalLicenses")

CommercialLicenses = model.addVar(vtype=GRB.INTEGER, name="CommercialLicenses")



### Define the constraints

model.addConstr(PersonalLicenses + CommercialLicenses <= MaxTotalLicenses)
model.addConstr(CostPersonalLicense * PersonalLicenses + CostCommercialLicense * CommercialLicenses <= MaxTotalExpenditure)
model.addConstr(PersonalLicenses >= 0)
model.addConstr(CommercialLicenses >= 0)


### Define the objective

model.setObjective(ProfitPersonalLicense * PersonalLicenses + ProfitCommercialLicense * CommercialLicenses, GRB.MAXIMIZE)


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
