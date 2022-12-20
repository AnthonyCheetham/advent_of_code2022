# Day 17 of Advent of Code 2022
import copy

with open("datasets/day17_input.dat","r") as myf:
    data = myf.read()

# Rocks with defined shapes falling down chasm and get blown side-to-side by wind
# Chasm is 7 units wide, infinitely tall and starts empty.
# Rocks stop falling permanently when any part tries to fall into a tile
# Part 1: What is the height after 2022 rocks?

shape_hitboxes = {
    "-":[[0,0],[1,0],[2,0],[3,0]],
    "+":[[1,0],[0,1],[2,1],[1,2],[1,1]],
    "L":[[0,0],[1,0],[2,0],[2,1],[2,2]],
    "|":[[0,0],[0,1],[0,2],[0,3]],
    "s":[[0,0],[1,0],[0,1],[1,1]],
}
rock_edges = { # Height and width of rock
    "-":[1,4],
    "+":[3,3],
    "L":[3,3],
    "|":[4,1],
    "s":[2,2],
}

class Rock(object):
    def __init__(self,y,type):
        # x,y is for the left-most and bottom-most edges
        self.x = 2
        self.y = y
        self.type = type
        self.shape = shape_hitboxes[type]
        self.h,self.w = rock_edges[type]

    def get_hitbox(self):
        """Return points taken up by the rock."""
        for p in self.shape:
            yield [p[0]+self.x,p[1]+self.y]

class Chamber(object):
    def __init__(self,input):
        # Process puzzle input
        sym_to_dir = {"<":-1,">":1} 
        self.jet = [sym_to_dir[x] for x in input]
        self.njet = len(self.jet)
        # Initialize variables we need, and chamber
        self.t = 0 # time
        self.height=0
        self.chamber = []
        for _ in range(7):
            self.chamber.append(7*["."])
        
        self.next_rock = "-"
        self.rock_order = {"-":"+", "+":"L", "L":"|", "|":"s", "s":"-"}
        self.rock = None
        self.rocks_added = 0
        self.new_rock_times = []
        self.removed_height = 0
        self.heights = []

    def __str__(self):
        s = ""
        temp_chamber = copy.deepcopy(self.chamber)
        if self.rock:
            for p in self.rock.get_hitbox():
                temp_chamber[p[1]][p[0]] = "@"
        for row in temp_chamber[::-1]:
            s += "|"+"".join(row)+"|"+"\n"
        s += "+-------+"
        return s

    def add_rock(self):
        self.rock = Rock(self.height+3,self.next_rock)
        self.next_rock = self.rock_order[self.next_rock]
        self.new_rock_times.append(self.t)
        self.heights.append(self.height+self.removed_height)


    def add_height(self,h):
        """Prep for next rock by extending the chamber up to fit it."""
        for _ in range(h):
            self.chamber.append(7*["."])
        self.height += max(0,h)

    def check_rock_collision(self):
        """Check if the falling rock is on top of something."""
        if self.rock.y < 0:
            return True
        for p in self.rock.get_hitbox():
            if self.chamber[p[1]][p[0]] == "#":
                return True
        return False

    def freeze_rock(self):
        """Freeze a rock in place and add it to the chamber."""
        # Extend grid
        self.add_height(self.rock.y+self.rock.h-self.height)
        # Add rock to the chamber
        for p in self.rock.get_hitbox():
            # assert self.chamber[p[1]][p[0]] == "." 
            self.chamber[p[1]][p[0]] = "#"
        self.rock = None # Reset rock
        self.rocks_added += 1

    def clean_up(self):
        """Look back a bit and remove sections we don't need to simulate."""
        try:
            # If a row has no air-gap then nothing below it matters 
            h = len(self.chamber) - 1 - self.chamber[::-1].index(7*["#"])
            self.removed_height += h+1
            self.chamber = self.chamber[h+1:]
            self.height -= (h+1)
            self.rock.y -= (h+1)
        except:
            pass

    def fast_tick(self):
        """Process the next rock."""
        # Make a rock
        self.add_rock()
        # Apply next 3 wind moves to rock
        for _ in range(3):
            wind = self.jet[self.t % self.njet]
            self.rock.x += wind
            # Keep within edges
            self.rock.x = max(0, self.rock.x)
            self.rock.x = min(7-self.rock.w, self.rock.x)
            self.t += 1
        # Move down 3
        self.rock.y -= 3

        # Now slowly apply steps until we collide
        collision = False
        while not collision:
            # Apply wind
            wind = self.jet[self.t % self.njet]
            oldx = self.rock.x
            self.rock.x += wind
            # Keep within edges
            self.rock.x = max(0, self.rock.x)
            self.rock.x = min(7-self.rock.w, self.rock.x)
            if self.check_rock_collision():
                self.rock.x = oldx 
            # Apply gravity
            self.rock.y -= 1
            if self.check_rock_collision():
                collision = True
                self.rock.y += 1
                self.freeze_rock()
            self.t += 1

        if self.rocks_added % 1000 == 0:
            self.clean_up()

c = Chamber(data)
while c.rocks_added < 2022:
    c.fast_tick()
print("Part 1:",c.height+c.removed_height)

# For Part 2, we need the height after 1,000,000,000,000 (1e12) rocks.
# This seems like it's implying there's a way to avoid simulating them all.
# I need to run it for a lot of rocks and then look for a pattern.
while c.rocks_added < 20000:
    c.fast_tick()

# Is there a pattern in the height increases?
# Could be any period and start after an unknown number of rocks 
offset = 5000 # Start a long way from the start to make sure we ignore burn-in
for l in range(100,5000):
    h1 = c.heights[offset:offset+l]
    h2 = c.heights[offset+l:offset+2*l]
    h3 = c.heights[offset+2*l:offset+3*l]
    h1= [h-h1[0] for h in h1]
    h2= [h-h2[0] for h in h2]
    h3= [h-h3[0] for h in h3]
    if h1 == h2 == h2:
        repeat_freq = l
        break

# Now find the burn-in offset when the repeating starts
for offset in range(2*repeat_freq):
    h1 = c.heights[offset:offset+repeat_freq]
    h2 = c.heights[offset+repeat_freq:offset+2*repeat_freq]
    h3 = c.heights[offset+2*repeat_freq:offset+3*repeat_freq]
    h1= [h-h1[0] for h in h1]
    h2= [h-h2[0] for h in h2]
    h3= [h-h3[0] for h in h3]
    if h1 == h2 == h3:
        break

## To calculate the height after n iterations we need to add
# the height of the burn-in period, the height due to the repeating
# cycles, and the height due to the last partial repeating cycle
iters = 1000000000000
extra_rocks = (iters - offset) % repeat_freq
n_repeats = (iters-offset)//repeat_freq

burn_in_height = c.heights[offset]
pattern_height = n_repeats*(c.heights[offset+2*repeat_freq] - c.heights[offset+repeat_freq])
unfinished_pattern_height = c.heights[offset+extra_rocks]-c.heights[offset]

total_height = burn_in_height + pattern_height + unfinished_pattern_height
print(f"Part 2: {total_height}")