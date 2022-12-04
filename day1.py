
with open("datasets/day1_input.dat") as myf:
    data = myf.read().splitlines()

# Find the elf carrying the most calories, and how much that is
# Each elf is separated by an empty line
# Keep a list of all the calories
calories = []
calories_running_tally = 0 # Will be reset for each elf
for line in data:
    if line == "":
        calories.append(calories_running_tally)
        calories_running_tally = 0
    else:
        calories_running_tally += int(line)
else:
    calories.append(calories_running_tally)

max_calories = max(calories)

# Part 1:
print("Max calories:",max_calories)

# Part 2:
calories.sort()
print("Top 3:",calories[-3]+calories[-2]+calories[-1])