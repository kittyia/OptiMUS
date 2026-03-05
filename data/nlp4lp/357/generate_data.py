import json
import numpy as np


def generate_hybrid_scheduling_data(
    num_students,
    num_classes,
    social_distancing_capacity,
    num_groups,
    E,
    num_time_slots,
    lambda_param,
    mu,
    seed=0,
):
    np.random.seed(seed)

    # Generate student and class lists
    students = [f"student{i+1}" for i in range(num_students)]
    classes = [f"class{j+1}" for j in range(num_classes)]

    # Generate enrollments for each class
    enrollments = {
        cls: np.random.choice(
            students, size=np.random.randint(1, num_students + 1), replace=False
        ).tolist()
        for cls in classes
    }

    # Generate social distancing capacities for each class
    capacities = {cls: social_distancing_capacity for cls in classes}

    # Generate classes scheduled to be ongoing at each time slot
    class_times = {
        t: np.random.choice(
            classes, size=np.random.randint(1, num_classes), replace=False
        ).tolist()
        for t in range(num_time_slots)
    }

    data = {
        "S": students,
        "C": classes,
        "A": enrollments,
        "c": capacities,
        "E": E,
        "G": num_groups,
        "T": num_time_slots,
        "C_t": class_times,
        "lambda": lambda_param,
        "mu": mu,
    }

    return data


# Parameters
num_students = 123
num_classes = 20
social_distancing_capacity = 7
num_groups = 4  # Four learning teams
E = 1
num_time_slots = 168  # 24 hours * 7 days
lambda_param = 0.25
mu = 0.1

# Generate data
data = generate_hybrid_scheduling_data(
    num_students,
    num_classes,
    social_distancing_capacity,
    num_groups,
    E,
    num_time_slots,
    lambda_param,
    mu,
)

# Save to JSON file
with open("data.json", "w") as f:
    json.dump(data, f, indent=4)

# Print JSON data
print(json.dumps(data, indent=4))
