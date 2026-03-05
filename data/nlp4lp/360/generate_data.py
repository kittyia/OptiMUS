import json
import numpy as np


def generate_rvrp_data(
    num_depots,
    num_tours,
    num_store_orders,
    num_lsp_tours,
    num_vehicles,
    num_common_carriers,
    seed=0,
):
    np.random.seed(seed)

    data = {
        "depots": [f"Depot_{i}" for i in range(num_depots)],
        "tours": [f"Tour_{i}" for i in range(num_tours)],
        "store_orders": [f"Order_{i}" for i in range(num_store_orders)],
        "lsp_tours": [f"LSP_{i}" for i in range(num_lsp_tours)],
        "vehicles": [f"Vehicle_{i}" for i in range(num_vehicles)],
        "common_carriers": [f"Carrier_{i}" for i in range(num_common_carriers)],
        "vehicle_limits": {
            f"LSP_{i}": {
                f"Vehicle_{j}": np.random.randint(1, 10) for j in range(num_vehicles)
            }
            for i in range(num_lsp_tours)
        },
        "tour_costs": {
            f"Tour_{i}": {
                f"LSP_{j}": np.random.randint(100, 500) for j in range(num_lsp_tours)
            }
            for i in range(num_tours)
        },
        "shipment_costs": {
            f"Order_{i}": {
                f"Carrier_{j}": np.random.randint(50, 200)
                for j in range(num_common_carriers)
            }
            for i in range(num_store_orders)
        },
        "tour_orders": {
            f"Order_{i}": [
                f"Tour_{j}"
                for j in np.random.choice(
                    num_tours, np.random.randint(1, 5), replace=False
                )
            ]
            for i in range(num_store_orders)
        },
        "tour_vehicles": {
            f"Vehicle_{i}": [
                f"Tour_{j}"
                for j in np.random.choice(
                    num_tours, np.random.randint(1, 5), replace=False
                )
            ]
            for i in range(num_vehicles)
        },
    }
    return data


# Parameters
num_depots = 3
num_tours = 10
num_store_orders = 20
num_lsp_tours = 5
num_vehicles = 4
num_common_carriers = 3

# Generate data
data = generate_rvrp_data(
    num_depots,
    num_tours,
    num_store_orders,
    num_lsp_tours,
    num_vehicles,
    num_common_carriers,
)

# Write JSON data to file
with open("data.json", "w") as f:
    json.dump(data, f, indent=4)

# Print JSON data
print(json.dumps(data, indent=4))
