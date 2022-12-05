# Day 5 of Advent of Code 2022

with open("datasets/day5_input.dat","r") as myf:
    data = myf.read().splitlines()

# Top of the input file is the arrangement of crates
# Bottom of the input file is the list of moves
split = data.index("")
top_part = data[0:split-1] # Bottom row is the stack numbers
instructions = data[split+1:]

# Work out the current arrangement of the crates
# How many crate stacks are there?
# Each stack will be a list, ordered from bottom to top, so stack[0] is bottom
n_stacks = (len(top_part[0])+1)//4
stacks = [[] for x in range(n_stacks)]
## Add crates to the stack starting from the bottom
for height,line in enumerate(top_part[::-1]):
    for stack in range(n_stacks):
        pos = int(4*stack+1)
        char = line[pos]
        if char != " ":
            stacks[stack].append(char)

## Now parse the instructions
def execute_move(stacks, instruction, part2=False):
    ## Assume form "move num from old to new"
    words = instruction.split(" ")
    num = int(words[1])
    old = int(words[3])-1 # Python starts at 0
    new = int(words[5])-1 # Python starts at 0

    # Now take them from the old stack
    crates = [stacks[old].pop() for _ in range(num)]

    # In part 2 they take a stack of crates instead of one at a time
    # So reverse the order
    if part2: 
        crates = crates[::-1]

    # Add them to the new
    stacks[new].extend(crates)

# Save a copy for part 2 below
stacks_part2 = [[c for c in stack] for stack in stacks]

## Part 1: Run all the instructions and work out whats on top
for inst in instructions:
    execute_move(stacks, inst)
on_top = "".join([s[-1] for s in stacks])
print("Part 1:", on_top)

## Part 2: Run all the instructions and work out whats on top
for inst in instructions:
    execute_move(stacks_part2, inst, part2=True)
on_top_part2 = "".join([s[-1] for s in stacks_part2])
print("Part 2:", on_top_part2)