# Day 16 of Advent of Code 2022
# Note: I cheated a bit on this one, by reading how others tackled it.
#       My original solution of treating it like a search problem and using
#       Dijkstra's algorithm worked for part 1, but took too long for part 2
#       And I ran out of ideas to optimize the search space.

with open("datasets/day16_input.dat","r") as myf:
    data = myf.read().splitlines()

# Network of tunnels, with valves in rooms between them.
# Each valve has a given flow rate.
# Takes 1 min to open a valve, 1 min to walk through a tunnel.
# Each valve stays open once it is opened, relieving 
# flow_rate*time_remaining total pressure
# What is the most pressure that can be relieved in 30mins?

# First make a map of which tunnels connect to which
connections = {}
useful_valves = []
useful_rates = []
rates = {}
for ix,line in enumerate(data):
    splits = line.split(" ")
    valve = splits[1]
    rate = int(splits[4].replace("rate=","").replace(";",""))
    tunnels = [x.replace(",","") for x in splits[9:]]
    # Save all this info 
    connections[valve] = tunnels
    if rate > 0:
        useful_valves.append(valve)
        useful_rates.append(rate)
        rates[valve] = rate

n_useful_valves = len(useful_valves)
valves_set = set(useful_valves)

## Now calculate shortest distance between any two useful valves
## (Plus the distance between any valve and AA)
def find_shortest_distance(v1,v2):
    # State is [location, dist_travelled]
    bfs_queue = [(v1,0)]
    visited = set(v1)
    while len(bfs_queue) > 0:
        state = bfs_queue.pop(0)
        # Where can we go next?
        options = connections[state[0]]
        if v2 in options:
            # Can we get to the desired destination from here?
            return state[1]+1
        new_states = [(v,state[1]+1) for v in options if v not in visited]
        bfs_queue.extend(new_states)
        visited = visited.union(set(options))

distances = {}
for v1_ix,v1 in enumerate(useful_valves):
    for v2 in useful_valves[v1_ix+1:]+["AA"]:
        d = find_shortest_distance(v1,v2)
        distances[(v1,v2)] = d
        distances[(v2,v1)] = d

## We can use this to find all possible paths between useful valves
## And then calculate their scores one-by-one.
## There's no point walking from A-B unless the goal is turn turn on valve B
## So we can just check paths between the useful valves.
def all_paths(distances, loc, valves_left, path, time_left):
    for v in valves_left:
       new_time = time_left - (distances[(loc,v)]+1)
       if new_time >= 0:
        yield from all_paths(distances,v,valves_left-{v},path+[v],new_time)
    yield path

def score_path(distances,rates,path,time_left):
    score = 0
    v1 = path[0]
    for v2 in path[1:]:
        time_left -= distances[(v1,v2)]+1 # Subtract walking and turning time
        assert time_left >= 0
        score += time_left*rates[v2] # Add points for releasing steam from now til the end
        v1 = v2 # Update position
    return score

# Find all possible paths through the valves within the time limit
paths = list(all_paths(distances,"AA",valves_set,["AA"],30))

## Now find the score for each one
scores = []
for p in paths:
    scores.append(score_path(distances,rates,p,30))
best_score = max(scores)
print("Part 1: Best score:",best_score)

## Part 2:
# Take 4 mins off but add an extra elephant that can open valves in the same way.
# We can look for all paths again, then take pairs that are mutually exclusive
# and find the best one
paths_part2 = list(all_paths(distances, "AA", valves_set, ["AA"], 26))
paths_sets_part2 = [set(p) for p in paths_part2] # Save a bit of run time
scores_part2 = [score_path(distances,rates,p,26) for p in paths_part2]
best_score_part2 = 0
for p1_ix, p1 in enumerate(paths_sets_part2):
    # If we're going to check all pairs like x1-x2 and x2-x1, this stops 
    # us from checking pairs starting with the low scoring one.
    # It drastically reduces run time
    if scores_part2[p1_ix] < (best_score_part2/2):
        continue

    for p2_ix, p2 in enumerate(paths_sets_part2):
        if len(p1.intersection(p2)) == 1:
            score = scores_part2[p1_ix] + scores_part2[p2_ix]
            best_score_part2 = max(best_score_part2,score)

print("Part 2: Best score:",best_score_part2)