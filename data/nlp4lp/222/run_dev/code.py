
import os
import numpy as np
import json 
from gurobipy import Model, GRB, quicksum


model = Model("OptimizationProblem")

with open("data.json", "r") as f:
    data = json.load(f)




### Define the parameters

PosterBoardsPerCircularTable = data["PosterBoardsPerCircularTable"] # shape: [], definition: Number of poster boards per circular table

ParticipantsPerCircularTable = data["ParticipantsPerCircularTable"] # shape: [], definition: Number of participants per circular table

GuestsPerCircularTable = data["GuestsPerCircularTable"] # shape: [], definition: Number of guests catered per circular table

SpacePerCircularTable = data["SpacePerCircularTable"] # shape: [], definition: Space units taken by one circular table

PosterBoardsPerRectangularTable = data["PosterBoardsPerRectangularTable"] # shape: [], definition: Number of poster boards per rectangular table

ParticipantsPerRectangularTable = data["ParticipantsPerRectangularTable"] # shape: [], definition: Number of participants per rectangular table

GuestsPerRectangularTable = data["GuestsPerRectangularTable"] # shape: [], definition: Number of guests catered per rectangular table

SpacePerRectangularTable = data["SpacePerRectangularTable"] # shape: [], definition: Space units taken by one rectangular table

MinimumParticipants = data["MinimumParticipants"] # shape: [], definition: Minimum number of participants to be accommodated

MinimumPosterBoards = data["MinimumPosterBoards"] # shape: [], definition: Minimum number of poster boards to be accommodated

AvailableSpace = data["AvailableSpace"] # shape: [], definition: Total available space units



### Define the variables

CircularTables = model.addVar(vtype=GRB.INTEGER, name="CircularTables")

RectangularTables = model.addVar(vtype=GRB.INTEGER, name="RectangularTables")



### Define the constraints

model.addConstr(
    ParticipantsPerCircularTable * CircularTables +
    ParticipantsPerRectangularTable * RectangularTables
    >= MinimumParticipants
)
model.addConstr(
    SpacePerCircularTable * CircularTables +
    SpacePerRectangularTable * RectangularTables
    <= AvailableSpace
)
model.addConstr(CircularTables >= 0)
model.addConstr(RectangularTables >= 0)
model.addConstr(CircularTables >= 0)
model.addConstr(RectangularTables >= 0)


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
