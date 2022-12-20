# Day 18 of Advent of Code 2022

with open("datasets/day18_input.dat","r") as myf:
    data = myf.read().splitlines()

# Each line of input is location of a 1x1x1 cube.
# Need to work out total exposed surface area of shape
# For each cube surface area should be (6 - n_neighbouring_cubes)

# Naively looping through is O(n**3)
# But if we can save them all to RAM should be O(n)
sz = 0
coords = []
for line in data:
    # Save the coordinates (but pad the array later by increasing them by 1)
    x,y,z = [int(a)+1 for a in line.split(",")]
    coords.append((x,y,z))
    sz = max(sz,x,y,z)
sz += 2 

grid = [[[False for x in range(sz)] for y in range(sz)] for z in range(sz)]
for x,y,z in coords:
    grid[z][y][x] = True

def neighbours(x,y,z):
    for dx in [-1,1]:
        yield (x+dx,y,z)
    for dy in [-1,1]:
        yield (x,y+dy,z)
    for dz in [-1,1]:
        yield (x,y,z+dz)
    
## Now for each point, check if the neighbouring points are filled
surface_area = 0
for x,y,z in coords:
    surface_area += 6
    for nx,ny,nz in neighbours(x,y,z):
        if grid[nz][ny][nx]:
            surface_area -= 1

print("Part 1:",surface_area)

## Part 2: Only look for external surfaces.
# Use a search algorithm. BFS should be fine since we need to explore everywhere
visited = [[[False for x in range(sz)] for y in range(sz)] for z in range(sz)]
def within_bounds(x,y,z,sz):
    if x < 0 or y < 0 or z < 0:
        return False
    if x >= sz or y >= sz or z >= sz:
        return False
    return True

to_visit = [(0,0,0)]
outside_surface_area = 0
while len(to_visit) > 0:
    x,y,z = to_visit.pop(0)

    # Find neighbouring points
    for nx,ny,nz in neighbours(x,y,z):
        # Ignore out of bounds or already visited points
        if not within_bounds(nx,ny,nz,sz):
            continue
        if visited[nz][ny][nx]:
            continue
        # If it's within the droplet count the surface area and move on
        if grid[nz][ny][nx]:
            outside_surface_area += 1
        else:
            to_visit.append((nx,ny,nz))
            visited[nz][ny][nx] = True
print("Part 2:",outside_surface_area)