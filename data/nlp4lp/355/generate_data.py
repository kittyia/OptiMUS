import json
import numpy as np

def generate_data(ship_options, prior_days, planning_horizon, locker_capacity, seed=0):
    np.random.seed(seed)
    data = {
        "ShipOptions": ship_options,
        "PriorDays": prior_days,
        "PlanningHorizon": planning_horizon,
        "LockerCapacity": locker_capacity,
        "DwellTimeProb": np.random.rand(ship_options, planning_horizon, planning_horizon).tolist(),
        "DwellTimeProbPrior": np.random.rand(ship_options, prior_days, planning_horizon).tolist(),
        "PackagesInLockerDayZero": np.random.randint(0, 10, size=(ship_options, prior_days)).tolist(),
        "Demand": np.random.randint(10, 35, size=(ship_options, planning_horizon)).tolist()
    }
    return data

# Parameters
ship_options = 2
prior_days = 7
planning_horizon = 10
locker_capacity = 100

# Generate data
data = generate_data(ship_options, prior_days, planning_horizon, locker_capacity)

# Print JSON data
with open("data.json", "w") as f:
    json_data = json.dump(data, f, indent=4)
print(json.dumps(data, indent=4))
