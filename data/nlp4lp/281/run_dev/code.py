
import os
import numpy as np
import json 
from gurobipy import Model, GRB, quicksum


model = Model("OptimizationProblem")

with open("data.json", "r") as f:
    data = json.load(f)




### Define the parameters

NumSchools = data["NumSchools"] # shape: [], definition: Total number of schools

NumGrades = data["NumGrades"] # shape: [], definition: Total number of grades

NumNeighborhoods = data["NumNeighborhoods"] # shape: [], definition: Total number of neighborhoods

Capacity = data["Capacity"] # shape: ['NumSchools', 'NumGrades'], definition: Capacity of school s for grade g

Population = data["Population"] # shape: ['NumNeighborhoods', 'NumGrades'], definition: Number of students of grade g in neighborhood n

Distance = data["Distance"] # shape: ['NumNeighborhoods', 'NumSchools'], definition: Distance from neighborhood n to school s



### Define the variables

Assignments = model.addVars(NumNeighborhoods, NumSchools, NumGrades, vtype=GRB.INTEGER, name="Assignments")



### Define the constraints

for n in range(NumNeighborhoods):
    for g in range(NumGrades):
        model.addConstr(
            sum(Assignments[n, s, g] for s in range(NumSchools)) == Population[n][g]
        )
for s in range(NumSchools):
    for g in range(NumGrades):
        model.addConstr(
            sum(Assignments[n, s, g] for n in range(NumNeighborhoods)) 
            <= Capacity[s][g]
        )
for n in range(NumNeighborhoods):
    for s in range(NumSchools):
        for g in range(NumGrades):
            model.addConstr(Assignments[n, s, g] >= 0)


### Define the objective

model.setObjective(
    quicksum(Distance[n][s] * Assignments[n, s, g]
             for n in range(NumNeighborhoods)
             for s in range(NumSchools)
             for g in range(NumGrades)),
    GRB.MINIMIZE
)


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
