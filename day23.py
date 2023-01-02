# Day 23 of Advent of Code 2022
from collections import defaultdict

with open("datasets/day23_input.dat","r") as myf:
    data = myf.read().splitlines()

# . = empty, # = elf
# empty ground outside of input
# Elves do:
# Step 1:
#  - If nobody is within the neighbouring 8 tiles, do nothing
#  - Look N,S,E,W. If nobody is in that or the diagonal squares, propose moving there
# Step 2:
#  - All elves move to their proposed positions simultaneously
#  - If two or more elves wanted to go to the same place, none move
# Step 3:
#  - Move the first direction in the list to the end
def bounding_box(elves, buffer=0):
    xs = [e[0] for e in elves]
    ys = [e[1] for e in elves]
    minx, maxx = min(xs)-buffer, max(xs)+buffer
    miny, maxy = min(ys)-buffer, max(ys)+buffer
    return minx,maxx,miny,maxy

def elves2board(elves,print_board=False,buffer=0):
    minx,maxx,miny,maxy = bounding_box(elves,buffer=buffer)
    nx,ny = maxx-minx+1, maxy-miny+1
    
    board = [["." for x in range(nx)] for y in range(ny)]
    for e in elves:
        board[e[1]-miny][e[0]-minx] = "#"
    if print_board:
        for line in board:
            print("".join(line))
    return board

def count_empty_ground(board):
    return sum([line.count(".") for line in board])

def get_moveable_elves(elves):
    elves_set = set(elves)
    moveable = [False for e in elves]
    for ix,e in enumerate(elves):
        for pos in [(-1,-1),(-1,0),(-1,1),(0,-1),(0,1),(1,-1),(1,0),(1,1)]:
            if (e[0]+pos[0],e[1]+pos[1]) in elves_set:
                moveable[ix] = True
                continue
    return moveable

def check_direction(e,direction,elves_set):
    # Check in list of elves (could also use board)
    x,y = direction
    to_check = [(x,y),(x+y,y+x),(x-y,y-x)]
    if x == 0:
        to_check = [(-1,y),(0,y),(1,y)]
    elif y == 0:
        to_check = [(x,-1),(x,0),(x,1)]
    else:
        print("uh oh!")
    for pos in to_check: # direction and diagonals
        if (e[0]+pos[0],e[1]+pos[1]) in elves_set:
            return False
    return True

def get_first_ok_direction(e, elves_set, directions):
    for d in directions:
        is_ok = check_direction(e,d,elves_set)
        if is_ok:
            return (e[0]+d[0], e[1]+d[1])
    return e

def get_moves(elves, directions, moveable):
    moves = []
    elves_set = set(elves)
    for ix,e in enumerate(elves):
        if moveable[ix]:
            new_e = get_first_ok_direction(e,elves_set,directions)
        else:
            new_e = e
        moves.append(new_e)
    return moves

def remove_collisions(moves, elves):
    moves_counts = defaultdict(int)
    for m in moves:
        moves_counts[m] += 1
    n = 0
    # Now remove invalid moves
    for ix,m in enumerate(moves):
        if moves_counts[m] > 1:
            moves[ix] = elves[ix]
            n += 1
    return moves    

def tick(elves,directions):
    moveable = get_moveable_elves(elves)
    if sum(moveable) == 0:
        return elves,directions,False
    moves = get_moves(elves,directions,moveable)
    new_elves = remove_collisions(moves,elves)
    directions.append(directions.pop(0))
    return new_elves,directions,True

# Load data and set up directions list
nx,ny = len(data[0]),len(data)
elves = [(x,y) for x in range(nx) for y in range(ny) if data[y][x]=="#"]
directions = [(0,-1),(0,1),(-1,0),(1,0)]

## Part 1:
## How many empty tiles within the smallest bounding box after 10 iterations

ix,n = 0,10
still_moving=True
while still_moving and ix < n:
    elves, directions,still_moving = tick(elves,directions)
    ix += 1
board = elves2board(elves,print_board=False)
print("Part 1:",count_empty_ground(board))

## Part 2:
## Keep simulating until it converges. How many iterations?
n = 100000 # Max iterations
still_moving=True
while still_moving and ix < n:
    elves, directions,still_moving = tick(elves,directions)
    ix += 1

print(f"Part 2: {ix} rounds to converge")