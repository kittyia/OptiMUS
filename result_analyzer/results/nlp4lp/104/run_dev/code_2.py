ython
import os
import json

with open("data.json", "r") as f:
    data = json.load(f)

# Parameters
FatApple = data["FatApple"]
FolateApple = data["FolateApple"]
FatCarrot = data["FatCarrot"]
FolateCarrot = data["FolateCarrot"]
AppleToCarrotRatio = data["AppleToCarrotRatio"]
MinCarrotServings = data["MinCarrotServings"]
MaxFolate = data["MaxFolate"]

# Since AppleServings = AppleToCarrotRatio * CarrotServings,
# substitute into folate constraint to find feasible range for CarrotServings.

# Total folate per unit of CarrotServings
folate_per_carrot = FolateApple * AppleToCarrotRatio + FolateCarrot

# Maximum feasible carrot servings based on folate constraint
max_carrot_servings = MaxFolate // folate_per_carrot

best_fat = -1
best_apple = 0
best_carrot = 0

for carrot in range(MinCarrotServings, int(max_carrot_servings) + 1):
    apple = AppleToCarrotRatio * carrot
    
    total_folate = FolateApple * apple + FolateCarrot * carrot
    if total_folate <= MaxFolate:
        total_fat = FatApple * apple + FatCarrot * carrot
        if total_fat > best_fat:
            best_fat = total_fat
            best_apple = apple
            best_carrot = carrot

if best_fat >= 0:
    print("Optimal Objective Value:", best_fat)
    with open("output_solution.txt", "w") as f:
        f.write(str(best_fat))
else:
    with open("output_solution.txt", "w") as f:
        f.write("No feasible solution found")
``