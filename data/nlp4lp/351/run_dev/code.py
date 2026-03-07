
import os
import numpy as np
import json 
from gurobipy import Model, GRB, quicksum


model = Model("OptimizationProblem")

with open("data.json", "r") as f:
    data = json.load(f)




### Define the parameters

FixedCosts = data["FixedCosts"] # shape: ['NumConsultants'], definition: Fixed cost for project j

AdditionalCosts = data["AdditionalCosts"] # shape: ['NumProjects', 'NumConsultants'], definition: Additional cost for assigning consultant i to project j

MaxProjectsPerConsultant = data["MaxProjectsPerConsultant"] # shape: [], definition: Maximum number of projects that can be assigned to a consultant

NumProjects = data["NumProjects"] # shape: [], definition: Number of projects

NumConsultants = data["NumConsultants"] # shape: [], definition: Number of consultants



### Define the variables

Assign = model.addVars(NumConsultants, NumProjects, vtype=GRB.BINARY, name="Assign")

Hire = model.addVars(NumConsultants, vtype=GRB.BINARY, name="Hire")



### Define the constraints

for i in range(NumProjects):
    model.addConstr(
        sum(Assign[j, i] for j in range(NumConsultants)) == 1
    )
for j in range(NumConsultants):
    model.addConstr(
        sum(Assign[j, i] for i in range(NumProjects)) <= MaxProjectsPerConsultant
    )
for j in range(NumConsultants):
    for i in range(NumProjects):
        model.addConstr(Assign[j, i] <= Hire[j])
for j in range(NumConsultants):
    for i in range(NumProjects):
        model.addConstr(Assign[j, i] >= 0)
        model.addConstr(Assign[j, i] <= 1)

for j in range(NumConsultants):
    model.addConstr(Hire[j] >= 0)
    model.addConstr(Hire[j] <= 1)


### Define the objective

model.setObjective(
    quicksum(FixedCosts[j] * Hire[j] for j in range(NumConsultants)) +
    quicksum(AdditionalCosts[i][j] * Assign[j, i]
             for i in range(NumProjects)
             for j in range(NumConsultants)),
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
