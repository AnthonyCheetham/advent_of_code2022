# Day 19 of Advent of Code 2022
from functools import cache

with open("datasets/day19_input.dat","r") as myf:
    data = myf.read().splitlines()

# Robot mining operation
# Input is a set of blueprints with costs for 4 materials -
#  ore, clay, obsidian and geodes
# Part 1: Work out which blueprint maximizes the number of opened geodes in 
# 24 mins

def process_cost_input(s):
    costs = [int(x) for x in s.split(" ") if x.isnumeric()]
    for x in range(4-len(costs)): # Pad to length 4
        costs.append(0)
    return tuple(costs)

def process_input_line(blueprint):
    # Process input
    blueprint = blueprint.split(":")[1]
    ore,clay,obsid,geode,_ = blueprint.split(".")

    ore_robot_costs = process_cost_input(ore)
    clay_robot_costs = process_cost_input(clay)
    obsidian_robot_costs = process_cost_input(obsid)
    geode_robot_costs = process_cost_input(geode)
    # Geodes cost ore and obsidian
    geode_robot_costs = (geode_robot_costs[0],0,geode_robot_costs[1],0)
    return (
        ore_robot_costs,
        clay_robot_costs,
        obsidian_robot_costs,
        geode_robot_costs,
    )
@cache
def is_robot_affordable(resources, robot_cost):
    return sum([a>=b for a,b in zip(resources,robot_cost)]) == 4

@cache
def which_are_affordable(resources, robot_costs):
    """Return list of indices for affordable robots."""
    return [
            ix for ix in range(4) if is_robot_affordable(resources, robot_costs[ix])
        ]

def dfs(robot_costs, total_time):
    """Return the most geodes that can be mined with a given time.
    Use a depth-first search so we can prune branches"""
    # Parametrize like:
    # 0-3 = amount of resources
    # 4-7 = number of robots
    # 8 = total time
    init_state = (0,0,0,0,1,0,0,0,total_time)
    queue = [init_state]
    n_geodes = 0
    states = 0
    states_set = set()
    states_set.add(init_state)
    max_costs = [max([r[i] for r in robot_costs]) for i in range(4)]
    max_costs[-1] = 999

    while len(queue) > 0:
        state = queue.pop(-1) # DFS
        res = state[0:4]
        robots = state[4:8]
        t = state[8]

        ## Iterate over trying to build each type of robot from here
        for b_ix in [0,1,2,3]:
            # ## No point trying to build a robot we will never afford
            if (b_ix == 2 and robots[1] == 0) or (b_ix == 3 and robots[2]==0):
                continue
            # And no point building anything other than a geode bot in the last minute
            if t <= 2 and b_ix != 3:
                continue
            # And no point building more robots than we need
            if robots[b_ix] >= max_costs[b_ix]:
                continue

            cost = robot_costs[b_ix]
            new_t = 1*t
            new_res = res
            while new_t > 0 and not is_robot_affordable(new_res,cost):
                new_res = tuple([a+b for a,b in zip(new_res,robots)])
                new_t -= 1
            
            if new_t == 0: 
                n_geodes = max(n_geodes, new_res[-1])
            elif new_t == 1: # No point actually building it
                new_res = tuple([a+b for a,b in zip(new_res,robots)])
                n_geodes = max(n_geodes, new_res[-1])
            else:
                ## Add resources for this turn and subtract robot cost
                new_res = tuple([a+b-c for a,b,c in zip(new_res,robots,cost)])
                new_robots = list(robots)
                new_robots[b_ix] += 1
                new_t -= 1
                new_state = tuple(new_res+tuple(new_robots)+(new_t,))

                # If there's only 1 min left then don't bother with the below
                if new_t == 1:
                    n_geodes = max(n_geodes, new_res[-1]+new_robots[-1])
                    continue

                # Is it worth pursuing this state?
                max_possible = new_res[-1] + new_robots[-1]*new_t + new_t*(new_t-1)//2
                if max_possible <= n_geodes:
                    continue

                # Only visit if we havent already
                if new_state not in states_set:
                    queue.append(new_state)
                    states_set.add(new_state)
                n_geodes = max(n_geodes, new_res[-1])
        states += 1
    return n_geodes

mins = 24
import time 
t0 = time.time()
quality_level = 0
for n in range(len(data)):
    robot_costs = process_input_line(data[n])
    n_geodes = dfs(robot_costs, mins)
    quality_level += (n+1)*n_geodes

print(f"Part 1: {quality_level}")

## Part 2:
## Run to 32 mins but only the first 3 blueprints
mins = 32
part2_score = 1
for n in range(len(data[0:3])):
    robot_costs = process_input_line(data[n])
    n_geodes = dfs(robot_costs, mins)
    part2_score *= n_geodes

print(f"Part 2: {part2_score}")