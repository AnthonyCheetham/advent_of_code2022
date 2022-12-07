# Day 6 of Advent of Code 2022

with open("datasets/day6_input.dat","r") as myf:
    data = myf.read() # Just one line today

# Part 1:
# Find the first position where 4 consecutive letters are different
# Loop through all of the groups of 4 letters
# For part 2 I parametrized the number 4 and set it to 14.
def find_marker(data, n=4):
    l = len(data)
    # Loop through every set of n characters
    for ix in range(l-n):
        chars = data[ix:ix+n]

        # Check each letter to see if it's in the remaining set
        has_pair = False
        for letter_ix in range(n-1): # Only need to check first 3
            in_first_part = chars[letter_ix] in chars[0:letter_ix]
            in_second_part = chars[letter_ix] in chars[letter_ix+1:] 
            if in_first_part or in_second_part:
                has_pair = True
        
        if not has_pair:
            print(f"Marker of length {n} at: {ix+n}")
            return ix+n

print("Part 1:")
find_marker(data, n=4)

print("Part 2:")
find_marker(data, n=14)