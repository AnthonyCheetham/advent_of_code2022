# Day 14 of Advent of Code 2022

with open("datasets/day14_input.dat","r") as myf:
    data = myf.read().splitlines()

# Simulate falling sand
# Puzzle input represents solid surfaces
# Looks like grid isn't too large to fit in memory

# First work out the minimum size we need to simulate
xmin,xmax = 500,500
ymax = 0
for line in data:
    for vals in line.split("->"):
        x,y = vals.split(",")
        x,y = int(x), int(y)
        xmin = min(xmin,x)
        xmax = max(xmax,x)
        ymax = max(ymax,y)

class Cave(object):
    def __init__(self,xmin,xmax,ymax,data,part2=False, buffer = 1):
        self.xoffset = xmin-buffer
        self.xmax = xmax-self.xoffset+2*buffer
        self.ymax = ymax + 2
        # Array to hold the state of the cave
        # Make an array thats (max-xmin+2) x (ymax+1) in size.
        # ymax+1 so that we can simulate things falling one tile into the abyss
        self.map = [["." for x in range(self.xmax+2)] for y in range(self.ymax+1)]
        # Add the sand source
        self.map[0][500-self.xoffset] = "+"
        self.source = (500-self.xoffset,0)
        self.n_sand = 0
        # Add the walls
        self.add_walls(data)
        # If part2, add a wall at the bottom
        if part2:
            self.map[-1] = ["#" for _ in self.map[-1]]

    def add_walls(self,data):
        for line in data:
            coords = line.split("->")
            for ix in range(len(coords)-1):
                x0,y0 = [int(c) for c in coords[ix].split(",")]
                x1,y1 = [int(c) for c in coords[ix+1].split(",")]

                x0 -= self.xoffset
                x1 -= self.xoffset
                # Add a wall between these points
                self.draw_wall_line(x0,y0,x1,y1)

    def draw_wall_line(self,x0,y0,x1,y1):
        dx = x1-x0
        dy = y1-y0
        if dx == 0:
            dir = dy//abs(dy)
            for y in range(y0,y1+dir,dir):
                self.map[y][x0] = "#"
        if dy == 0:
            dir = dx//abs(dx)
            for x in range(x0,x1+dir,dir):
                self.map[y0][x] = "#"

    def __str__(self):
        """Displays the current state of the cave for debugging."""
        big_str = ""
        for line in self.map:
            big_str += "".join(line)+"\n"
        return big_str
    
    def drop_sand(self):
        """Adds a new drop of sand. Returns False if it stopped in the grid."""
        x,y = self.source
        still_moving = True
        while still_moving and y < self.ymax:
            newy = y+1
            if self.map[newy][x] == ".":
                y = newy
            elif self.map[newy][x-1] == ".":
                y = newy
                x = x-1
            elif self.map[newy][x+1] == ".":
                y = newy
                x = x+1
            else:
                # It stops here
                self.map[y][x] = "o"
                still_moving = False
        # If we filled to the top, also stop
        if y == 0:
            still_moving = True
        # If we went off the grid, give an error
        if x < 0 or (x>=self.xmax):
            raise Exception("Grid too small")
                
        return still_moving
    
    def fill_with_sand(self):
        """Keep adding sand until it falls off the edge."""
        fell_into_abyss = False
        while not fell_into_abyss:
            fell_into_abyss = self.drop_sand()
            # Add sand if fell_into_abyss is False
            self.n_sand += 1-1*fell_into_abyss


cave = Cave(xmin, xmax, ymax, data)
cave.fill_with_sand()
# print(cave)
print("Part 1:",cave.n_sand)

# Part 2:
# Add an infinite floor at ymax+2 and keep filling until it hits the roof
# Or... add a lot of buffer to the sides instead of infinite, and give
# an error if it's too small, so I can just increase the size until the
# grid is large enough to handle the pile of sand
cave2 = Cave(xmin, xmax, ymax, data, part2=True, buffer=150)
cave2.fill_with_sand()
print("Part 2:",cave2.n_sand+1) # +1 for the one that ended in the source