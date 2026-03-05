import json
import numpy as np


def generate_data(
    seed: int = 0,
    L: int = 5,
    K: int = 3,
    T: int | None = None,
    max_orders_per_period: int = 5,
    max_pool_size: int = 1000,
    max_fulfillment_orders: int = 1000,
    cost_scale: float = 1.0,
):
    """Generate synthetic data that is guaranteed to be feasible with the
    current optimization model (without changing the model).

    Parameters
    - seed: random seed
    - L: maximum stay in the pool (int)
    - K: number of probability groups (int)
    - T: last period (int). If None, defaults to (L+1)+10
    - max_orders_per_period: cap on arrivals per period (int)
    - max_pool_size: pool capacity per period (int)
    - max_fulfillment_orders: max flow per period (int)
    - cost_scale: scale for c_F coefficients (float)

    Returns a data dictionary with string time keys to match model access.
    """

    np.random.seed(seed)

    # Compute dependent dimensions
    t = L + 1
    if T is None:
        T = t + 10

    # Basic validation & safety adjustments
    if max_pool_size < max_orders_per_period * (L + 1):
        max_pool_size = max_orders_per_period * (L + 1)
    if max_fulfillment_orders < max_orders_per_period:
        max_fulfillment_orders = max_orders_per_period

    # Multiorder group probabilities (small, non-negative)
    p = [float(x) * 0.2 for x in np.random.rand(K).tolist()]

    # Orders arriving in each period (modest random arrivals)
    I = {
        str(tau): int(np.random.randint(0, max_orders_per_period + 1))
        for tau in range(t, T + 1)
    }

    # Set I_prime to zeros (no forced existing pool content)
    I_prime = {str(tau): [0 for _ in range(K)] for tau in range(t, T + 1)}

    # Set epsilon to zeros so no unexpected 'hits' reduce S_prime
    epsilon = {
        str(tau): {
            str(s): [0 for _ in range(K)] for s in range(max(t - L, tau - L), tau + 1)
        }
        for tau in range(t, T + 1)
    }

    # Provide a benign initial O (all zeros)
    O = {
        str(tau): {
            str(s): [0 for _ in range(K)] for s in range(max(t - L, tau - L), tau)
        }
        for tau in range(t, T + 1)
    }

    # Pool size and max flow
    C = {str(tau): int(max_pool_size) for tau in range(t, T + 1)}
    F_bar = {str(tau): int(max_fulfillment_orders) for tau in range(t, T + 1)}

    # Small per-period penalty coefficients
    c_F = {
        str(tau): float(0.1 * np.random.rand() * cost_scale) for tau in range(t, T + 1)
    }

    data = {
        "I": I,
        "I_prime": I_prime,
        "epsilon": epsilon,
        "O": O,
        "C": C,
        "F_bar": F_bar,
        "p": p,
        "c_F": c_F,
        "T": T,
        "L": L,
        "K": K,
        "t": t,
    }

    # Save a copy for inspection
    try:
        with open("data.json", "w") as f:
            json.dump(data, f, indent=4)
    except Exception:
        pass

    return data


data = generate_data()
# Save to JSON file
with open("data.json", "w") as f:
    json.dump(data, f, indent=4)
