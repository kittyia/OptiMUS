import json
from gurobipy import Model, GRB, quicksum

# Read inputs from JSON file
with open("data.json", "r") as f:
    inputs = json.load(f)

depots = inputs["depots"]
tours = inputs["tours"]  # I
store_orders = inputs["store_orders"]  # K
lsp_tours = inputs["lsp_tours"]  # J
vehicles = inputs["vehicles"]  # V
common_carriers = inputs["common_carriers"]  # N
vehicle_limits = inputs["vehicle_limits"]
tour_costs = inputs["tour_costs"]  # c_ij
shipment_costs = inputs["shipment_costs"]  # c_kn
tour_orders = inputs["tour_orders"]  # I_k
tour_vehicles = inputs["tour_vehicles"]  # V_i

# Create a new model
model = Model("R-VRP_Optimization")

# Decision variables
x = model.addVars(
    tours, lsp_tours, vtype=GRB.BINARY, name="x"
)  # Tours assigned to LSPs
y = model.addVars(
    store_orders, common_carriers, vtype=GRB.BINARY, name="y"
)  # Single shipments with common carriers

# Objective function: Minimize the total transportation cost
model.setObjective(
    quicksum(tour_costs[i][j] * x[i, j] for i in tours for j in lsp_tours)
    + quicksum(
        shipment_costs[k][n] * y[k, n] for k in store_orders for n in common_carriers
    ),
    GRB.MINIMIZE,
)

# Constraints
# Ensure that each store order is either fulfilled via a delivery tour or shipped with a common carrier
for k in store_orders:
    model.addConstr(
        quicksum(x[i, j] for i in tour_orders[k] for j in lsp_tours)
        + quicksum(y[k, n] for n in common_carriers)
        == 1,
        name=f"Fulfillment_{k}",
    )

# Enforce truck availability restrictions
for j in lsp_tours:
    for v in vehicles:
        model.addConstr(
            quicksum(x[i, j] for i in tour_vehicles[v]) <= vehicle_limits[j][v],
            name=f"TruckAvailability_{j}_{v}",
        )

# Ensure that total tours assigned to LSP do not exceed available vehicles
for j in lsp_tours:
    model.addConstr(
        quicksum(x[i, j] for i in tours) <= sum(vehicle_limits[j][v] for v in vehicles),
        name=f"TotalTours_{j}",
    )

# Optimize the model
model.optimize()

# Extract results
if model.status == GRB.OPTIMAL:
    print(f"Obj: {model.objVal}")
    from pathlib import Path

    Path("obj.txt").write_text(str(model.objVal))
else:
    print("No optimal solution found.")
