
import os
import numpy as np
import json 
from gurobipy import Model, GRB, quicksum


model = Model("OptimizationProblem")

with open("data.json", "r") as f:
    data = json.load(f)




### Define the parameters

TotalMoney = data["TotalMoney"] # shape: [], definition: Total amount of money available to gamble

NumBets = data["NumBets"] # shape: [], definition: Number of different sports bets

LossProbabilities = data["LossProbabilities"] # shape: ['NumBets'], definition: Chance of losing money for each sport bet

Payouts = data["Payouts"] # shape: ['NumBets'], definition: Payout per dollar for each sport bet

MaxAverageLossProbability = data["MaxAverageLossProbability"] # shape: [], definition: Maximum average chance of losing money



### Define the variables

BetAmounts = model.addVars(NumBets, vtype=GRB.CONTINUOUS, name="BetAmounts")



### Define the constraints

model.addConstr(sum(BetAmounts[i] for i in range(NumBets)) <= TotalMoney)
model.addConstr(
    sum(LossProbabilities[i] * BetAmounts[i] for i in range(NumBets))
    <= MaxAverageLossProbability * TotalMoney
)
for i in range(NumBets):
    model.addConstr(BetAmounts[i] >= 0)


### Define the objective

model.setObjective(quicksum(Payouts[i] * BetAmounts[i] for i in range(NumBets)), GRB.MAXIMIZE)


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
