# Day 8 of Advent of Code 2022

with open("datasets/day8_input.dat","r") as myf:
    data = myf.read().splitlines()

### Each value is the height of a tree
# Part 1:
# How many trees are visible?
nx = len(data[0])
ny = len(data)

xs = list(range(nx))
ys = list(range(ny))
# List to keep track of which ones are visible
visible = [[0 for x in xs] for y in ys]

# Go through left to right and right to left
for y in ys:
    # Left to right
    maxh = -1
    for x in xs:
        h = int(data[y][x])
        if h > maxh:
            visible[y][x] = 1
            maxh = h

    # Right to left
    maxh = -1
    for x in xs[::-1]:
        h = int(data[y][x])
        if h > maxh:
            visible[y][x] = 1
            maxh = h

# Go through top to bottom and bottom to top
for x in xs:
    # Top to bottom
    maxh = -1
    for y in ys:
        h = int(data[y][x])
        if h > maxh:
            visible[y][x] = 1
            maxh = h

    # Bottom to top
    maxh = -1
    for y in ys[::-1]:
        h = int(data[y][x])
        if h > maxh:
            visible[y][x] = 1
            maxh = h

num_visible = sum([sum(y) for y in visible])
print("Part 1:", num_visible)

## Part 2:
# For each position, scenic_score = multiple of viewing distance in each direction
posx,posy=2,1
def get_scenic_score(data, posx, posy):
    """Calculate the scenic score from a given position."""
    viewing_dists = []
    maxh = int(data[posy][posx])
    # Look left
    dist = 0
    for x in range(posx-1,-1,-1):
        h = int(data[posy][x])
        dist += 1
        if h >= maxh:
            break
    viewing_dists.append(dist)

    # Look right
    dist = 0
    for x in range(posx+1,nx,1):
        h = int(data[posy][x])
        dist += 1
        if h >= maxh:
            break
    viewing_dists.append(dist)

    # Look up
    dist = 0
    for y in range(posy-1,-1,-1):
        h = int(data[y][posx])
        dist += 1
        if h >= maxh:
            break
    viewing_dists.append(dist)

    # Look down
    dist = 0
    for y in range(posy+1,ny,1):
        h = int(data[y][posx])
        dist += 1
        if h >= maxh:
            break
    viewing_dists.append(dist)

    scenic_score = 1
    for dist in viewing_dists:
        scenic_score *= dist
    return scenic_score

## Find the best scenic score
best_score = 0
for posx in xs:
    for posy in ys:
        score = get_scenic_score(data, posx, posy)
        best_score = max(score, best_score)

print("Part 2:", best_score)