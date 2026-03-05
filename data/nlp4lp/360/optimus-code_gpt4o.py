import json
from gurobipy import *

# Load data
with open("data.json", "r") as f:
    data = json.load(f)

# Extract data
depots = data["depots"]
tours = data["tours"]
store_orders = data["store_orders"]
lsp_tours = data["lsp_tours"]
vehicles = data["vehicles"]
common_carriers = data["common_carriers"]
vehicle_limits = data["vehicle_limits"]
tour_costs = data["tour_costs"]
shipment_costs = data["shipment_costs"]
tour_orders = data["tour_orders"]
tour_vehicles = data["tour_vehicles"]

# Create model
model = Model("R-VRP")

# Decision variables
x = model.addVars(tours, lsp_tours, vtype=GRB.BINARY, name="x")
y = model.addVars(store_orders, common_carriers, vtype=GRB.BINARY, name="y")

# Objective: Minimize total transportation cost
model.setObjective(
    quicksum(tour_costs[t][j] * x[t, j] for t in tours for j in lsp_tours) +
    quicksum(shipment_costs[k][n] * y[k, n] for k in store_orders for n in common_carriers),
    GRB.MINIMIZE
)

# Constraints
# Each store order is either fulfilled via a delivery tour or shipped with a common carrier
for k in store_orders:
    model.addConstr(
        quicksum(x[t, j] for t in tour_orders[k] for j in lsp_tours) +
        quicksum(y[k, n] for n in common_carriers) == 1,
        name=f"order_fulfillment_{k}"
    )

# Truck availability restrictions
for j in lsp_tours:
    for v in vehicles:
        model.addConstr(
            quicksum(x[t, j] for t in tour_vehicles.get(v, [])) <= vehicle_limits[j][v],
            name=f"vehicle_limit_{j}_{v}"
        )

# Optimize model
model.optimize()

# Write solution to solution.json
solution = {
    "variables": {
        "x": {f"{t}_{j}": x[t, j].X for t in tours for j in lsp_tours if x[t, j].X > 0.5},
        "y": {f"{k}_{n}": y[k, n].X for k in store_orders for n in common_carriers if y[k, n].X > 0.5}
    },
    "objective": model.objVal
}

with open("solution.json", "w") as f:
    json.dump(solution, f, indent=4)
