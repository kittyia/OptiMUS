
import os
import numpy as np
import json 
from gurobipy import Model, GRB, quicksum


model = Model("OptimizationProblem")

with open("data.json", "r") as f:
    data = json.load(f)




### Define the parameters

MinCalcium = data["MinCalcium"] # shape: [], definition: Minimum required units of calcium

MinVitaminMix = data["MinVitaminMix"] # shape: [], definition: Minimum required units of vitamin mix

MinProtein = data["MinProtein"] # shape: [], definition: Minimum required units of protein

PriceRegular = data["PriceRegular"] # shape: [], definition: Price per bag of regular brand

PricePremium = data["PricePremium"] # shape: [], definition: Price per bag of premium brand

CalciumRegular = data["CalciumRegular"] # shape: [], definition: Units of calcium per bag of regular brand

CalciumPremium = data["CalciumPremium"] # shape: [], definition: Units of calcium per bag of premium brand

VitaminMixRegular = data["VitaminMixRegular"] # shape: [], definition: Units of vitamin mix per bag of regular brand

VitaminMixPremium = data["VitaminMixPremium"] # shape: [], definition: Units of vitamin mix per bag of premium brand

ProteinRegular = data["ProteinRegular"] # shape: [], definition: Units of protein per bag of regular brand

ProteinPremium = data["ProteinPremium"] # shape: [], definition: Units of protein per bag of premium brand



### Define the variables

RegularBags = model.addVar(vtype=GRB.INTEGER, name="RegularBags")

PremiumBags = model.addVar(vtype=GRB.INTEGER, name="PremiumBags")



### Define the constraints

model.addConstr(CalciumRegular * RegularBags + CalciumPremium * PremiumBags >= MinCalcium)
model.addConstr(VitaminMixRegular * RegularBags + VitaminMixPremium * PremiumBags >= MinVitaminMix)
model.addConstr(RegularBags >= 0)
model.addConstr(PremiumBags >= 0)


### Define the objective

model.setObjective(PriceRegular * RegularBags + PricePremium * PremiumBags, GRB.MINIMIZE)


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
