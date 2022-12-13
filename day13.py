# Day 13 of Advent of Code 2022

with open("datasets/day13_input.dat","r") as myf:
    data = myf.read().split("\n\n")

# Compare the lists with a recursive function
def compare_vals(packet1, packet2):
    """Will return:
        True if they're clearly in the right order
        False if they're clearly not in the right order,
        None if it's unclear from the inputs."""
    # print("Comparing:",packet1, packet2)
    # If one is a list and the other is an integer, pretend they're both lists
    if type(packet1) != type(packet2):
        if isinstance(packet1,int):
            packet1 = [packet1]
        else:
            packet2 = [packet2]

    # If they're integers, lowest value should be first
    if isinstance(packet1,int) and isinstance(packet2,int):
        if packet1 < packet2:
            return True
        elif packet1 == packet2:
            # We can't say
            return None
        else:
            return False
    # If they're both lists, compare their elements
    elif isinstance(packet1,list) and isinstance(packet2,list):
        # Then compare them element by element
        while len(packet1) > 0 and len(packet2) > 0:
            val1 = packet1.pop(0)
            val2 = packet2.pop(0)
            outcome =  compare_vals(val1, val2)
            if outcome is not None:
                return outcome
        # If we ran out of items in one or more lists
        if len(packet1) == 0 and len(packet2) == 0:
            return None
        elif len(packet1) == 0:
            return True
        elif len(packet2) == 0:
            return False
    else:
        print("unknown:",packet1,packet2)
    return None

def in_right_order(packet1,packet2):
    """Works out if str1 and str2 are in the right order."""
    outcome = compare_vals(packet1, packet2)
    if outcome is None:
        outcome = True
    return outcome

index_sum = 0
for ix,pair in enumerate(data):
    str1,str2 = pair.splitlines()
    # Live dangerously and blindly execute the input so we have them as lists
    packet1,packet2 = [],[] # Stop VSCode complaining about undefined variables
    exec("packet1 = "+str1)
    exec("packet2 = "+str2)
    outcome = in_right_order(packet1,packet2)
    if outcome:
        index_sum += (ix+1)
print(f"Part 1: Pairs in right order have index sum: {index_sum}")

## Part 2:
# Use this function in a sorting algorithm with two additional inputs,
# Then find where they ended up
# Get the input ready
sorted_input = []
for pair in data:
    str1
    sorted_input.extend(pair.splitlines())
# Add divider packets
sorted_input.append("[[2]]")
sorted_input.append("[[6]]")
n_packets = len(sorted_input)
# Do a simple bubble sort, and we can upgrade if needed
not_in_order = True
loop = 0 # In case I need to see how far it got in a given time
while not_in_order:
    not_in_order = False
    loop += 1
    # Loop through all pairs, swapping them if not in order
    for ix in range(n_packets-1):
        str1 = sorted_input[ix]
        str2 = sorted_input[ix+1]
        # Live dangerously and blindly execute the input so we have them as lists
        packet1,packet2 = [],[] # Stop VSCode complaining about undefined variables
        exec("packet1 = "+str1)
        exec("packet2 = "+str2)

        pairwise_right_order = in_right_order(packet1,packet2)

        if not pairwise_right_order:
            sorted_input[ix] = str2
            sorted_input[ix+1] = str1
            not_in_order = True
# Find where the divider packets ended up
decoder_key = 1
for ix,str in enumerate(sorted_input):
    if str in ["[[2]]","[[6]]"]:
        decoder_key *= (ix+1)
print(f"Part 2: {decoder_key}")