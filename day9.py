# Day 9 of Advent of Code 2022

with open("datasets/day9_input.dat","r") as myf:
    data = myf.read().splitlines()

# Define up and right as +ve directions
dir_to_move = {
    "R": (1,0),
    "L": (-1,0),
    "U": (0,1),
    "D": (0,-1),
}

class RopeHead(object):
    def __init__(self):
        self.x = 0
        self.y = 0
        self.tail = None
    
    def add_tail(self):
        if self.tail is None:
            self.tail = RopeTail(self)
        else:
            new_tail = self.tail.add_tail()

    def update_tail(self):
        self.tail.update()

    def parse_movement(self, line):
        """Update the position of the rope."""
        dir, dist = line.split(" ")
        dist = int(dist)

        # Move the head a number of steps
        for _ in range(dist):
            # Move head
            movex, movey = dir_to_move[dir]
            self.x += movex
            self.y += movey

            # Update tail
            self.update_tail()

class RopeTail(RopeHead):
    def __init__(self, head):
        self.x = 0
        self.y = 0
        self.visited = set([(self.x,self.y)])
        self.head = head
        self.tail = None

    def update(self):
        """Move this rope tail to catch up to its head."""
        dx = self.head.x - self.x
        dy = self.head.y - self.y

        moved = False
        if (abs(dx) + abs(dy)) > 2:
            # Move diagonal
            self.x += dx//abs(dx)
            self.y += dy//abs(dy)
            moved = True
        elif abs(dx) > 1:
            # Move left/right
            self.x += dx//abs(dx)
            moved=True
        elif abs(dy) > 1:
            # Move up/down
            self.y += dy//abs(dy)
            moved = True
        
        if moved:
            self.visited.add((self.x, self.y))
            # And update its tail
            if self.tail is not None:
                self.tail.update()

## Part 1:
rope = RopeHead()
rope.add_tail()
for movement in data:
    rope.parse_movement(movement)

print("Part 1:",len(rope.tail.visited))

## Part 2:
rope2 = RopeHead()
for _ in range(9):
    rope2.add_tail()
for movement in data:
    rope2.parse_movement(movement)
# I could have added a "get_tail_visited" function
# But I like how visual this is
print("Part 2:",len(rope2.tail.tail.tail.tail.tail.tail.tail.tail.tail.visited))