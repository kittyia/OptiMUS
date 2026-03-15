
import os
import numpy as np
import json 
from gurobipy import Model, GRB, quicksum


model = Model("OptimizationProblem")

with open("data.json", "r") as f:
    data = json.load(f)




### Define the parameters

CoffeePowderPerMocha = data["CoffeePowderPerMocha"] # shape: [], definition: Amount of coffee powder required to produce one mocha

MilkPerMocha = data["MilkPerMocha"] # shape: [], definition: Amount of milk required to produce one mocha

CoffeePowderPerRegularCoffee = data["CoffeePowderPerRegularCoffee"] # shape: [], definition: Amount of coffee powder required to produce one regular coffee

MilkPerRegularCoffee = data["MilkPerRegularCoffee"] # shape: [], definition: Amount of milk required to produce one regular coffee

AvailableCoffeePowder = data["AvailableCoffeePowder"] # shape: [], definition: Total available units of coffee powder

AvailableMilk = data["AvailableMilk"] # shape: [], definition: Total available units of milk

TimePerMocha = data["TimePerMocha"] # shape: [], definition: Time taken to produce one mocha

TimePerRegularCoffee = data["TimePerRegularCoffee"] # shape: [], definition: Time taken to produce one regular coffee

MochaToRegularRatio = data["MochaToRegularRatio"] # shape: [], definition: Minimum multiple of mochas required compared to regular coffees



### Define the variables

MochaQuantity = model.addVar(vtype=GRB.INTEGER, name="MochaQuantity")

RegularCoffeeQuantity = model.addVar(vtype=GRB.INTEGER, name="RegularCoffeeQuantity")



### Define the constraints

model.addConstr(MilkPerMocha * MochaQuantity + MilkPerRegularCoffee * RegularCoffeeQuantity <= AvailableMilk)
model.addConstr(MochaQuantity >= MochaToRegularRatio * RegularCoffeeQuantity)
model.addConstr(MochaQuantity >= 0)
model.addConstr(RegularCoffeeQuantity >= 0)


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
