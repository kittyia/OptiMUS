
import os
import numpy as np
import json 
from gurobipy import Model, GRB, quicksum


model = Model("OptimizationProblem")

with open("data.json", "r") as f:
    data = json.load(f)




### Define the parameters

TransportRateEscalator = data["TransportRateEscalator"] # shape: [], definition: Transport rate of an escalator in people per minute

TransportRateElevator = data["TransportRateElevator"] # shape: [], definition: Transport rate of an elevator in people per minute

SpaceEscalator = data["SpaceEscalator"] # shape: [], definition: Space taken by an escalator in units

SpaceElevator = data["SpaceElevator"] # shape: [], definition: Space taken by an elevator in units

MinPeopleTransport = data["MinPeopleTransport"] # shape: [], definition: Minimum number of people to transport per minute

RatioEscalatorsToElevators = data["RatioEscalatorsToElevators"] # shape: [], definition: Minimum ratio of escalators to elevators

MinElevators = data["MinElevators"] # shape: [], definition: Minimum number of elevators to be installed



### Define the variables

numberEscalators = model.addVar(vtype=GRB.INTEGER, name="numberEscalators")

numberElevators = model.addVar(vtype=GRB.INTEGER, name="numberElevators")



### Define the constraints

model.addConstr(TransportRateEscalator * numberEscalators + TransportRateElevator * numberElevators >= MinPeopleTransport)
model.addConstr(numberEscalators >= RatioEscalatorsToElevators * numberElevators)
model.addConstr(numberElevators >= MinElevators)
model.addConstr(numberEscalators >= 0)
model.addConstr(numberElevators >= 0)


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
