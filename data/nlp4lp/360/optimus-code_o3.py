import json
from gurobipy import *

# 1. -------------------------------------------------
with open("data.json", "r") as f:
    data = json.load(f)

# sets ------------------------------------------------
Tours     = data["tours"]
Orders    = data["store_orders"]
LSPs      = data["lsp_tours"]
Vehicles  = data["vehicles"]
Carriers  = data["common_carriers"]

# helper dictionaries --------------------------------
U   = data["vehicle_limits"]             # vehicle limits per LSP
cij = data["tour_costs"]                 # cost tour i, LSP j
ckn = data["shipment_costs"]             # cost order k, carrier n
I_k = data["tour_orders"]                # tours that can serve order k
V_i_raw = data.get("tour_vehicles", {})  # vehicles that can run tour

# build vehicle-to-tours and tour-to-vehicles maps ----
tour_to_vehicles = {t: [] for t in Tours}
for v, tours in V_i_raw.items():
    for t in tours:
        tour_to_vehicles.setdefault(t, []).append(v)

# any tour without vehicle assignment gets dummy type -
DUMMY_VEHICLE = "NoType"
for t in Tours:
    if not tour_to_vehicles[t]:
        tour_to_vehicles[t] = [DUMMY_VEHICLE]
if DUMMY_VEHICLE not in Vehicles:
    Vehicles.append(DUMMY_VEHICLE)

# 2. model -------------------------------------------
model = Model("RVRP_assignment")
model.Params.OutputFlag = 0  # silence Gurobi output

#  variables -----------------------------------------
x = {}  # x[i,j,v] = 1 if tour i executed by LSP j with vehicle v
for i in Tours:
    for v in tour_to_vehicles[i]:
        for j in LSPs:
            var = model.addVar(vtype=GRB.BINARY,
                               name=f"x[{i},{j},{v}]")
            x[(i, j, v)] = var

y = {}  # y[k,n] = 1 if order k shipped via carrier n
for k in Orders:
    for n in Carriers:
        var = model.addVar(vtype=GRB.BINARY,
                           name=f"y[{k},{n}]")
        y[(k, n)] = var

model.update()

#  constraints ---------------------------------------

# 2.1 each tour executed at most once
for i in Tours:
    expr = quicksum(x[i, j, v]
                    for v in tour_to_vehicles[i]
                    for j in LSPs)
    model.addConstr(expr <= 1, name=f"tour_once[{i}]")

# 2.2 vehicle availability per LSP
for j in LSPs:
    for v in Vehicles:
        if v == DUMMY_VEHICLE:
            continue  # unlimited dummy vehicles
        limit = U.get(j, {}).get(v, 0)
        expr = quicksum(x[i, j, v]
                        for i in Tours
                        if v in tour_to_vehicles[i])
        model.addConstr(expr <= limit,
                        name=f"veh_limit[{j},{v}]")

# 2.3 each order served exactly once
for k in Orders:
    tours_cover = I_k.get(k, [])
    expr_tours = quicksum(
        x[i, j, v]
        for i in tours_cover
        for v in tour_to_vehicles[i]
        for j in LSPs
    )
    expr_car   = quicksum(y[k, n] for n in Carriers)
    model.addConstr(expr_tours + expr_car == 1,
                    name=f"cover[{k}]")

#  objective -----------------------------------------
obj_tours = quicksum(
    cij[i][j] * x[i, j, v]
    for i in Tours
    for v in tour_to_vehicles[i]
    for j in LSPs
)
obj_shipments = quicksum(
    ckn[k][n] * y[k, n]
    for k in Orders
    for n in Carriers
)
model.setObjective(obj_tours + obj_shipments, GRB.MINIMIZE)

# 3. --------------------------------------------------
model.optimize()

# 4. write solution ----------------------------------
solution = {"variables": {}, "objective": model.objVal}
for var in model.getVars():
    if var.X > 1e-6:  # only store non-zero decisions
        solution["variables"][var.VarName] = var.X

with open("solution.json", "w") as f:
    json.dump(solution, f, indent=4)
