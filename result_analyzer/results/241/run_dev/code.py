
import os
import numpy as np
import json 
from gurobipy import Model, GRB, quicksum


model = Model("OptimizationProblem")

with open("data.json", "r") as f:
    data = json.load(f)




### Define the parameters

FreightCapacityPerTrip = data["FreightCapacityPerTrip"] # shape: [], definition: Amount of tons freight can transport per trip

AirCapacityPerTrip = data["AirCapacityPerTrip"] # shape: [], definition: Amount of tons air can transport per trip

FreightCostPerTrip = data["FreightCostPerTrip"] # shape: [], definition: Cost per freight trip in dollars

AirCostPerTrip = data["AirCostPerTrip"] # shape: [], definition: Cost per air trip in dollars

MinimumTotalTons = data["MinimumTotalTons"] # shape: [], definition: Minimum total tons to transport

Budget = data["Budget"] # shape: [], definition: Budget for transportation in dollars

MinimumAirProportion = data["MinimumAirProportion"] # shape: [], definition: Minimum proportion of tons to transport via air

MinimumFreightTrips = data["MinimumFreightTrips"] # shape: [], definition: Minimum number of freight trips



### Define the variables

FreightTrips = model.addVar(vtype=GRB.INTEGER, name="FreightTrips")

AirTrips = model.addVar(vtype=GRB.INTEGER, name="AirTrips")



### Define the constraints

model.addConstr(FreightCapacityPerTrip * FreightTrips + AirCapacityPerTrip * AirTrips >= MinimumTotalTons)
model.addConstr(FreightCostPerTrip * FreightTrips + AirCostPerTrip * AirTrips <= Budget)
model.addConstr(
    AirCapacityPerTrip * AirTrips >=
    MinimumAirProportion * (FreightCapacityPerTrip * FreightTrips + AirCapacityPerTrip * AirTrips)
)
model.addConstr(FreightTrips >= MinimumFreightTrips)
model.addConstr(AirTrips >= 0)


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
