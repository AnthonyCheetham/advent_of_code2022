# Day 22 of Advent of Code 2022

with open("datasets/day22_input.dat","r") as myf:
    data = myf.read().splitlines()

# Parse the input
board = data[:-2]
nx = max([len(line) for line in board])
ny = len(board)
# Make the board a rectangle
board = [line+(nx-len(line))*" " for line in board]
# Find the edges in each row and column 
edgesx = [
    (
        min(line.index("."), line.find("#")%nx),
        max(line.rindex("."), line.rfind("#"))
        ) for line in board
    ]
board_transpose = list(zip(*board))
board_transpose = ["".join(x) for x in board_transpose]
edgesy = [
    (
        min(line.index("."), line.find("#")%nx),
        max(line.rindex("."), line.rfind("#"))
        ) for line in board_transpose
    ]
direction_string = data[-1]
directions = []
new_dir = ""
for c in direction_string:
    if c in "RL":
        directions.append(new_dir)
        directions.append(c)
        new_dir = ""
    else:
        new_dir += c
directions.append(new_dir)
directions = [d for d in directions if d != ""] ## Temp
facing2step = {0:[1,0], 1:[0,1], 2:[-1,0], 3:[0,-1]}
facing2sym = {0:">",1:"v",2:"<",3:"^"}
def wrap(x,y,facing,edgesx,edgesy):
    if facing in [0,2]: # Horizontal move
        x = wrap_coords_2d(x,y,edgesx)
    else: # Vertical move
        y = wrap_coords_2d(y,x,edgesy)
    return x,y,facing

def wrap_coords_2d(a,b, edges):
    if a < edges[b][0]:
        a = edges[b][1]
    elif a > edges[b][1]:
        a = edges[b][0]
    return a

# Follow directions to move through the board
# Position is [x,y,direction]
# direction: 0 = right, 1=down, 2=left, 3=up
x,y,facing = board[0].index("."), 0, 0
for d in directions:
    if d == "R":
        facing = (facing + 1) % 4
    elif d == "L":
        facing = (facing -1) % 4
    else:
        d = int(d)
        step = facing2step[facing]
        # Move
        for ix in range(d):
            newx = (x + step[0])# % nx
            newy = (y + step[1])# % ny
            # Check if new pos is on grid
            newx,newy,newfacing = wrap(newx,newy,facing,edgesx,edgesy)
            # Check if it's a wall
            if board[newy][newx] == "#":
                break
            elif board[newy][newx] == " ":
                print(f"Invalid position! ({newx},{newy})")
                raise Exception
            x,y,facing = newx,newy,newfacing # Then it's valid, so move there
print("Part 1:",1000*(y+1)+4*(x+1)+facing)

## Part 2:
# It's actually a cube flattened out, so when walking off the grid
# we need to move to what would be the adjacent face
face_size = min([b-a for a,b in edgesx])+1
def walk_3d(x,y,newx,newy,facing,edgesx,edgesy,face_size):
    # Check if we walked off the edge
    if newx < 0 or newx >= nx:
        walked_off_x, walked_off_y = True,False
    elif newy < 0 or newy >= ny:
        walked_off_x, walked_off_y = False, True
    else:
        walked_off_x = (newx < edgesx[newy][0]) or (newx > edgesx[newy][1])
        walked_off_y = (newy < edgesy[newx][0]) or (newy > edgesy[newx][1])
    if walked_off_x or walked_off_y:
        return walk_to_next_face(x,y,newx,newy,facing,face_size)
    return newx,newy,facing

def rotate(x,y,n,face_size):
    """Rotate n times"""
    for _ in range(n):
        x,y = y,-x-1
    return x % face_size, y % face_size

def walk_to_next_face(x,y,newx,newy,facing,face_size):
    face_coords = (x//face_size, y//face_size)
    # face_map[face_coords][facing] returns new face_coords
    # and the facing of the edge you enter into 
    face_map = { # None means it's connected
        (1,0):[None,None,((0,2),2),((0,3),2)],
        (2,0):[((1,2),0),((1,1),0),None,((0,3),1)],
        (1,1):[((2,0),1),None,((0,2),3),None],
        (0,2):[None,None,((1,0),2),((1,1),2)],
        (1,2):[((2,0),0),((0,3),0),None,None],
        (0,3):[((1,2),1),((2,0),3),((1,0),3),None],
        }
    new_face,direction = face_map[face_coords][facing]
    new_facing = (direction+2) % 4
    # Apply rotation needed to enter new face
    n_rotations = (2+facing-direction) % 4
    dx,dy = x % face_size, y % face_size # position on face
    newdx, newdy = rotate(dx,dy,n_rotations,face_size)
    # Walk into the new face
    step = facing2step[new_facing]
    newdx = (newdx + step[0]) % face_size
    newdy = (newdy + step[1]) % face_size
    # Now fix the coordinates so we're actually on that face
    newx = face_size*new_face[0] + newdx
    newy = face_size*new_face[1] + newdy
    return newx,newy,new_facing

### Same loop but with different functions
x,y,facing = board[0].index("."), 0, 0
for d in directions:
    if d == "R":
        facing = (facing + 1) % 4
    elif d == "L":
        facing = (facing -1) % 4
    else:
        d = int(d)
        # Move
        for ix in range(d):
            step = facing2step[facing]
            newx = (x + step[0])
            newy = (y + step[1])
            newx,newy,newfacing = walk_3d(x,y,newx,newy,facing,edgesx,edgesy,face_size)
            # Check if it's a wall
            if board[newy][newx] == "#":
                break
            elif board[newy][newx] == " ":
                print(f"Invalid position! ({newx},{newy})")
                raise Exception
            x,y,facing = newx,newy,newfacing # Then it's valid, so move there
print("Part 2:",1000*(y+1)+4*(x+1)+facing)