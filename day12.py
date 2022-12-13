# Day 11 of Advent of Code 2022

with open("datasets/day12_input.dat","r") as myf:
    data = myf.read().splitlines()

# Hill climbing
# Will want to do breadth-first search or Dijkstra's algorithm
# Parametrize the state at any instance by (x, y) position and steps taken
# Then make a queue/list of states to check, and an array of positions visited

## Part 1:
# Clean up the map
map = [[x for x in line] for line in data]
map_size = (len(map[0]), len(map)) # x,y size
# Make a list to track visited or queued positions 
visited = [[False for _ in line] for line in map]

# Find the start and end position
for y, line in enumerate(map):
    for x, val in enumerate(line):
        if val == "S":
            xstart = x
            ystart = y
            map[y][x]="a"
        elif val == "E":
            xend = x
            yend = y
            map[y][x]="z"

# Make a list of states to check next. Start with current position
possible_moves = [(xstart,ystart,0)]

# Make a function to check if we can move there
def move_is_possible(x, y, newx, newy, part2=False):
    # Check outside of map
    if newx < 0 or newy < 0 or newx > (map_size[0]-1) or newy > (map_size[1]-1):
        return False
    # Check visited
    if visited[newy][newx]:
        return False
    # Check we aren't climbing more than 1 higher
    if not part2:
        if (ord(map[newy][newx]) - ord(map[y][x])) <= 1:
            return True
    else:
        # For part 2 we're walking backwards
        if (ord(map[y][x]) - ord(map[newy][newx])) <= 1:
            return True

# Go through the list until we find the position we want or run out of options
print("Part 1:")
while len(possible_moves) > 0:
    x,y,steps = possible_moves.pop(0)
    # Stop if we made it
    if x == xend and y == yend:
        print(f"  Made it in {steps} moves!")
        break

    # Work out where we can walk to, add it to the list and mark as visited
    for newx, newy in [(x+1,y),(x-1,y),(x,y+1),(x,y-1)]:
        if move_is_possible(x,y,newx,newy):
            possible_moves.append((newx,newy,steps+1))
            visited[newy][newx] = True
    if len(possible_moves) == 0:
        print("  Ran out of moves! :( ")

## Part 2:
# This time we don't have to start at S, but can be anywhere with elevation "a"
# Could try all "a" starting locations, but instead I'll reverse the problem 
# and start at the top and walk down, then stop when the first path reaches "a"
possible_moves = [(xend,yend,0)]
visited = [[False for _ in line] for line in map]
visited[yend][xend] = True

# Go through the list until we find the position we want or run out of options
print("Part 2:")
while len(possible_moves) > 0:
    x,y,steps = possible_moves.pop(0)
    # Stop if we made it to elevation "a"
    if map[y][x] == "a":
        print(f"  Made it in {steps} moves!")
        break

    # Work out where we can walk to, add it to the list and mark as visited
    for newx, newy in [(x+1,y),(x-1,y),(x,y+1),(x,y-1)]:
        if move_is_possible(x, y, newx, newy, part2=True):
            possible_moves.append((newx,newy,steps+1))
            visited[newy][newx] = True
    if len(possible_moves) == 0:
        print("  Ran out of moves! :( ")