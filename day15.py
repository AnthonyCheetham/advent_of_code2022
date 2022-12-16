# Day 15 of Advent of Code 2022

with open("datasets/day15_input.dat","r") as myf:
    data = myf.read().splitlines()

# List of positions of sensors and their closest beacon positions.

grid_size = (50,50)
grid = [["." for x in range(grid_size[0])] for y in range(grid_size[1])]

# Save all the locations
sensors = []
beacons = []
distances = [] # (x+y) distances between them
for line in data:
    sensor_text,beacon_text = line.split(":")
    
    sensorx, sensory = sensor_text.replace("Sensor at x=","").split(", y=")
    sensorx, sensory = int(sensorx), int(sensory)
    sensors.append((sensorx, sensory))
    
    beaconx, beacony = beacon_text.replace("closest beacon is at x=","").split(", y=")
    beaconx, beacony = int(beaconx), int(beacony)
    beacons.append((beaconx, beacony))

    distances.append(abs(beaconx-sensorx)+abs(beacony-sensory))
n_sensors = len(distances)
## What is the min and max x and y coords?
minx = min([sensors[ix][0]-distances[ix] for ix in range(n_sensors)])
maxx = max([sensors[ix][0]+distances[ix] for ix in range(n_sensors)])
miny = min([sensors[ix][1]-distances[ix] for ix in range(n_sensors)])
maxy = max([sensors[ix][1]+distances[ix] for ix in range(n_sensors)])

## To calculate the entire grid would be impractical, since the search area goes
## close to 7M squares in each direction
## Instead, consider a line and work out for each sensor which points are ruled out
y = 2000000 # The row to check
# y = 10 # For test set
covered = set()
# Check each sensor
for s_ix in range(n_sensors):
    # Which squares are ruled out?
    # We know how much of the search distance is taken up by the y distance
    d = distances[s_ix]-abs(y-sensors[s_ix][1])
    if d >= 0:
        for x in range(sensors[s_ix][0]-d,sensors[s_ix][0]+d+1):
            covered.add((x,y))
# Now remove any beacons from the set
for b in beacons:
    if b in covered:
        covered.remove(b)
print("Part 1:",len(covered))

## Part 2:
# Beacon is between 0 - 4M. Find the remaining square it could be in
# Options: 
# 1. Try the line solution above and repeat it for 2M iterations? Impractical.
# 2. While loop. Go through sensors. If one covers this area, jump to the first
#    square outside the range then repeat
coordmax = 4000000
# coordmax = 20 ## For test input

x,y = 0,0
found_beacon = False
### Loop that finds the first sensor each time
while found_beacon is False and y <= coordmax:
    # Go through sensors to see if this square is ruled out
    found_beacon=True
    for s_ix in range(n_sensors):
        # Does it reach this point?
        x_dist = abs(x-sensors[s_ix][0])
        y_dist = abs(y-sensors[s_ix][1])
        if (x_dist+y_dist) <= distances[s_ix]:
            found_beacon=False
            # Then move to the next available space
            x = sensors[s_ix][0]+distances[s_ix]-y_dist+1
            # Or back to the start of the row if we can rule out the rest of this row
            if x > coordmax:
                x = 0
                y += 1
            break
if y > coordmax:
    print("Didnt find it up to",x,y)
else:
    print("Found at",x,y)
    print("Part 2:",x*4000000+y)