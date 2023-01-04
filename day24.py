# Day 24 of Advent of Code 2022

with open("datasets/day24_input.dat","r") as myf:
    data = myf.read().splitlines()

# Input represents blizzards in a valley, with direction indicated.
# Blizzards move and then wrap to other side.
# They can stack, and move through each other unimpeded
# What is the quickest time to reach the opposite end?

# Goal:
# 1. Simulate blizzard for n steps and cache results
#    - Keep a map for each of left facing, right facing, up facing and down 
#      facing blizzards. This is easy to simulate.
#    - Then convert to a flat map, which is easy for the search to parse
# 2. Run a BFS with no backwards movement, taking the blizzard at time t for each one.
#    - If needed, can take an A*-like approach and do a DFS-like search ordered by 
#      distance to end and time taken

class Valley(object):
    def __init__(self,data):
        self.init_map = data
        self.parse_input()
        self.map_cache = {0:self.init_map}
        self.max_turns = 0  # Maximum turns simulated
        self.motion = {
            "v":(0,1),
            "^":(0,-1),
            "<":(-1,0),
            ">":(1,0)
            }

    def parse_input(self):
        self.blizzards = {
            "<":[],">":[],"^":[],"v":[]
        }
        for y,line in enumerate(self.init_map):
            for x,c in enumerate(line):
                if c in "><^v":
                    self.blizzards[c].append((x,y))
        self.nx = len(self.init_map[0])
        self.ny = len(self.init_map)

    def get_blank_valley(self):
        blank_valley = [[c for c in self.init_map[0]]]
        for _ in range(self.ny-2):
            blank_valley.append(["#"]+(self.nx-2)*["."]+["#"])
        blank_valley.append([c for c in self.init_map[-1]])
        return blank_valley

    def wrap(self,coord,size):
        return ((coord-1) % (size-2)) + 1
    
    def sim_turn(self):
        # Move all of the blizzards
        for sym in ["<",">","^","v"]:
            movex, movey = self.motion[sym]
            for ix,(x,y) in enumerate(self.blizzards[sym]):
                if sym in ["<",">"]:
                    self.blizzards[sym][ix] = (self.wrap(x+movex,self.nx),y)
                else:
                    self.blizzards[sym][ix] = (x,self.wrap(y+movey,self.ny))
        # Make a map and save it
        valley = self.get_blank_valley()
        for sym in self.blizzards:
            for (x,y) in self.blizzards[sym]:
                sym_in_pos = valley[y][x]
                if sym_in_pos == ".":
                    valley[y][x] = sym
                elif sym_in_pos in "><v^":
                    valley[y][x] = "2"
                elif sym_in_pos in "23":
                    valley[y][x] = str(int(sym_in_pos)+1)
                else:
                    print("Unknown symbol:",sym_in_pos)
        self.max_turns += 1
        self.map_cache[self.max_turns] = valley

    def print_valley(self,turn=0):
        valley = self.map_cache[turn]
        for line in valley:
            print("".join(line))

n = 1500
valley = Valley(data) 
for ix in range(n):
    valley.sim_turn()

def get_moves(state,valley):
    t,x,y = state
    next_map = valley.map_cache[t+1]
    moves = []
    # Can we stand still?
    if next_map[y][x] == ".":
        moves.append((t+1,x,y))
    # Can we move in each dir?
    for dx,dy in [(-1,0),(1,0),(0,-1),(0,1)]:
        if next_map[y+dy][x+dx] == ".":
            moves.append((t+1,x+dx,y+dy))
    return moves

def search_for_best_route(start_state, goal_pos, valley, maxiters = 1500000):
    queue = [start_state] # Start
    visited = set()
    visited.add(queue[0])
    iters = 0
    bestt = -1
    while (len(queue) > 0) and (iters < maxiters):
        state = queue.pop(0)

        # Check if we made it:
        if (state[1],state[2]) == goal_pos:
            bestt = state[0]
            break

        new_moves = get_moves(state,valley)

        # Remove any bad ones and mark them as visited
        for m_ix,m in enumerate(new_moves):
            # Don't repeat
            if m in visited:
                new_moves.pop(m_ix)
            else:
                visited.add(m)
            
        queue.extend(new_moves)
        iters += 1
    if bestt == -1:
        print(f"Didnt make it within t<{state[0]} :(")
    return bestt

# Part 1:
# What is the quickest time you can get to the exit?
# state vector is (t,x,y)
# To avoid worrying about edge effects, I'll start inside the grid 
# and end in the opposite corner, then add 1 minute to take the final step
goal_pos = (valley.nx-2, valley.ny-2)
bestt = search_for_best_route((1,1,1),goal_pos,valley)
print("Part 1:",bestt+1,"minutes to reach goal")

## Part 2:
# What is the quickest way to walk there, back to the start and then back to the end again
# Just start again from end position 
start_pos = (1, 1)
new_start = (bestt+2, goal_pos[0], goal_pos[1])
bestt2 = search_for_best_route(new_start, start_pos, valley)

# Then go back again
new_start = (bestt2+2, 1, 1)
bestt3 = search_for_best_route(new_start, goal_pos, valley)
print("Part 2:",bestt3+1,"minutes total")