# Advent of code Day 4

with open("datasets/day4_input.dat","r") as myf:
    data = myf.read().splitlines()

# Each line is two ranges of numbers

## Part 1:
# How many pairs have one set completely contained by the other?
num_contained = 0
for line in data:
    elf1, elf2 = line.split(",")
    elf1 = [int(x) for x in elf1.split("-")]
    elf2 = [int(x) for x in elf2.split("-")]

    if elf1[0] <= elf2[0] and elf1[1] >= elf2[1]:
        num_contained += 1
    elif elf2[0] <= elf1[0] and elf2[1] >= elf1[1]:
        num_contained += 1
print("Part 1:", num_contained)

## Part 2:
# How many pairs contain ranges that overlap at all?
num_overlap = 0
for line in data:
    elf1, elf2 = line.split(",")
    elf1 = [int(x) for x in elf1.split("-")]
    elf2 = [int(x) for x in elf2.split("-")]

    # It's easier to check if they don't overlap
    if not (elf1[1] < elf2[0] or elf1[0] > elf2[1]):
        num_overlap += 1
print("Part 2:", num_overlap)