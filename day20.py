# Day 20 of Advent of Code 2022

with open("datasets/day20_input.dat","r") as myf:
    data = myf.read().splitlines()

# Each line of input is a number. Go through the list and move each 
# number ahead or backwards by its value. Do so in the order they originally
# appeared in the list.

def mix_with_order(data, order=None):
    n = len(data)
    if order is None: # To keep track of the order we need to move them
        order = list(range(n))

    for num_ix in range(n):
        current_pos = order.index(num_ix)
        num = data.pop(current_pos)
        _ = order.pop(current_pos)
        # Calculate new position
        new_pos = current_pos + num
        new_pos = new_pos % (n-1)
        # Move it to new position in both order list and data list
        data.insert(new_pos, num)
        order.insert(new_pos, num_ix)
    return data, order

## Part 1:
# Find the 1000th, 2000th and 3000th number after 0
data_pt1 = [int(d) for d in data]
data_pt1,_ = mix_with_order(data_pt1)
pos_of_zero = data_pt1.index(0)
ix1 = (pos_of_zero + 1000) % len(data_pt1)
ix2 = (pos_of_zero + 2000) % len(data_pt1)
ix3 = (pos_of_zero + 3000) % len(data_pt1)
print(f"Part 1: {data_pt1[ix1]+data_pt1[ix2]+data_pt1[ix3]}")

## Part 2:
# Multiply each number by 811589153 then mix 10 times.
# But process each number based on their original order.
# So I just need to track where each number moved to with another list
data_pt2 = [int(d)*811589153 for d in data]
order_pt2 = list(range(len(data_pt2)))
for rep in range(10):
    data_pt2,order_pt2 = mix_with_order(data_pt2,order_pt2)
pos_of_zero = data_pt2.index(0)
ix1 = (pos_of_zero + 1000) % len(data_pt2)
ix2 = (pos_of_zero + 2000) % len(data_pt2)
ix3 = (pos_of_zero + 3000) % len(data_pt2)
print(f"Part 2: {data_pt2[ix1]+data_pt2[ix2]+data_pt2[ix3]}")