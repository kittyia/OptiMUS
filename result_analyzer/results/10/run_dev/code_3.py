import json

# Available stock
max_apples = 10
max_bananas = 20
max_grapes = 80

best_profit = 0
best_B = 0
best_C = 0

# Since stock is small, we can brute-force all feasible integer combinations
for B in range(0, max_apples // 6 + 1):
    for C in range(0, max_apples // 5 + 1):
        apples_used = 6 * B + 5 * C
        bananas_used = 6 * C
        grapes_used = 30 * B + 20 * C
        
        if (apples_used <= max_apples and
            bananas_used <= max_bananas and
            grapes_used <= max_grapes):
            
            profit = 6 * B + 7 * C
            
            if profit > best_profit:
                best_profit = profit
                best_B = B
                best_C = C

# Output optimal objective value
with open("output_solution.txt", "w") as f:
    f.write(str(best_profit))