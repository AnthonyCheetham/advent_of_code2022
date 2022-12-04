# Advent of code day 3
with open("datasets/day3_input.dat","r") as myf:
    data = myf.read().splitlines()

# Each line of the input is a list of items.
# First half is for compartment 1, second half for compartment 2

def get_priority(item):
    # Priority is 1-26 for a-z, 27-52 for A-Z
    # ord() encodes a-z into integers (but not starting at 0)
    priority = ord(item.lower())-ord("a")+1
    # Fix lowercase
    if item.lower() != item:
        priority += 26
    return priority

## Part 1:
# Find the sum of values for items that are in both compartments

running_score = 0
for line in data:
    
    n_items = len(line)
    compartment1 = line[0:n_items//2]
    compartment2 = line[n_items//2:]

    # This is trivial in python because of sets
    items_in_1 = set(compartment1)
    items_in_2 = set(compartment2)

    items_in_both = items_in_1.intersection(items_in_2)
    item_in_both = items_in_both.pop()
    
    running_score += get_priority(item_in_both)
print("Part 1:", running_score)

## Part 2:
# Each group of 3 lines contains one letter in common
# Find the sum of priorities for these common letters
running_badge_tally = 0
n_lines = len(data)
for ix in range(n_lines//3):
    
    line1 = data[3*ix]
    line2 = data[3*ix+1]
    line3 = data[3*ix+2]

    # This is also trivial in python because of sets
    items_in_bag1 = set(line1)
    items_in_bag2 = set(line2)
    items_in_bag3 = set(line3)

    items_in_all = items_in_bag1.intersection(items_in_bag2).intersection(items_in_bag3)
    common_item = items_in_all.pop()
    
    running_badge_tally += get_priority(common_item)
print("Part 2:", running_badge_tally)