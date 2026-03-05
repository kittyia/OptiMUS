import json
import numpy as np

# Function to generate more interesting data
def generate_interesting_data(J, M, N, seed=0):
    np.random.seed(seed)
    
    # Generate random input data x_m_j with different ranges
    x_m_j = (np.random.rand(M, J) * 2 - 1).tolist()
    
    # Generate random output data y_n_j with a specific relationship to x_m_j
    y_n_j = (np.random.rand(N, J) * 2 - 1).tolist()
    
    # Introduce a relationship: make y_n_j somewhat related to x_m_j
    for j in range(J):
        for n in range(N):
            y_n_j[n][j] += 0.5 * np.sum([x_m_j[m][j] for m in range(M)]) / M

    # Create the data dictionary
    data = {
        "J": J,
        "M": M,
        "N": N,
        "x_m_j": x_m_j,
        "y_n_j": y_n_j
    }
    
    return data

# Example usage
data = generate_interesting_data(J=5, M=3, N=5)

# Write the data to a JSON file
with open("data.json", "w") as f:
    json.dump(data, f, indent=4)
print(json.dumps(data, indent=4))
