
import os
import numpy as np
import json 
from gurobipy import Model, GRB, quicksum


model = Model("OptimizationProblem")

with open("data.json", "r") as f:
    data = json.load(f)




### Define the parameters

RegularBoatCapacity = data["RegularBoatCapacity"] # shape: [], definition: Number of pieces of mail a regular boat can carry per trip

RegularBoatGasConsumption = data["RegularBoatGasConsumption"] # shape: [], definition: Amount of gas (liters) used by a regular boat per trip

SpeedBoatCapacity = data["SpeedBoatCapacity"] # shape: [], definition: Number of pieces of mail a speed boat can carry per trip

SpeedBoatGasConsumption = data["SpeedBoatGasConsumption"] # shape: [], definition: Amount of gas (liters) used by a speed boat per trip

MaxRegularBoatTrips = data["MaxRegularBoatTrips"] # shape: [], definition: Maximum number of trips that can be made by regular boats

MinFractionSpeedBoatTrips = data["MinFractionSpeedBoatTrips"] # shape: [], definition: Minimum required fraction of trips to be made by speed boats

TotalMail = data["TotalMail"] # shape: [], definition: Total number of pieces of mail to be delivered



### Define the variables

RegularBoatTrips = model.addVar(vtype=GRB.INTEGER, name="RegularBoatTrips")

SpeedBoatTrips = model.addVar(vtype=GRB.INTEGER, name="SpeedBoatTrips")



### Define the constraints

model.addConstr(RegularBoatCapacity * RegularBoatTrips + SpeedBoatCapacity * SpeedBoatTrips >= TotalMail)
model.addConstr(RegularBoatTrips <= MaxRegularBoatTrips)
model.addConstr(SpeedBoatTrips >= RegularBoatTrips)
model.addConstr(RegularBoatTrips >= 0)
# RegularBoatTrips is defined as an integer variable (vtype=GRB.INTEGER),
# so no additional constraint is required to enforce integrality.
model.addConstr(SpeedBoatTrips >= 0)


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
