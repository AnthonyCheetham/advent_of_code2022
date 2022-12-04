with open("datasets/day2_input.dat","r") as myf:
    data = myf.read().splitlines()

# Rock-paper-scissors
# I'll define 1=rock, 2=paper, 3=scissors (which matches the score we'll need)
# And the outcome of a round as 0=loss, 1=draw, 2=win

def translate_shape(shape:str):
    shape_map = {
        "A":1,
        "B":2,
        "C":3,
        "X":1,
        "Y":2,
        "Z":3,
    }
    return shape_map[shape]

def calculate_score(shape_int:int, outcome:int):
    """Calculate score of a given round of rock/paper/scissors."""
    return shape_int + 3*outcome
    
def determine_result(our_shape_int:int, their_shape_int:int):
    "Decide who won a round of rock paper scissors."
    # To win, we need our shape to be 1 greater than their shape, mod 3
    # i.e. 2 beats 1,
    diff = (our_shape_int - their_shape_int) % 3
    if diff == 1:
        return 2
    elif diff == 0:
        return 1
    else:
        return 0

def score_one_game(line):
    """Calculate score from one game."""
    # Parse shapes
    their_shape, our_shape = line.split(" ")
    their_shape_int = translate_shape(their_shape)
    our_shape_int = translate_shape(our_shape)

    # Work out who won and score the game
    outcome = determine_result(our_shape_int, their_shape_int)
    score = calculate_score(our_shape_int, outcome)
    return score

## Functions for part 2
def translate_outcome(outcome_str:str):
    outcome_map = {
        "X":0,
        "Y":1,
        "Z":2,
    }
    return outcome_map[outcome_str]

def pick_shape_given_outcome(their_shape_int, outcome):
    """Given the shape they chose and a desired outcome, decide which shape."""
    # To win, you want their_shape + 1. To lose you want their shape -1
    our_shape_int = (their_shape_int+outcome-1) % 3
    # But python mod 3 will give numbers 0-2, when we want 1-3
    if our_shape_int == 0:
        our_shape_int = 3
    return our_shape_int

def score_one_game_part2(line):
    """Calculate score from one game, if the second symbol is the outcome."""
    # Parse shapes
    their_shape, outcome_str = line.split(" ")
    their_shape_int = translate_shape(their_shape)
    outcome = translate_outcome(outcome_str)

    # Work out which symbol to choose
    our_shape_int = pick_shape_given_outcome(their_shape_int, outcome)
    score = calculate_score(our_shape_int, outcome)
    return score

## Part 1:
# Calculate score for each game assuming second column is also rock/paper/scissors
score = 0
for line in data:
    score += score_one_game(line)
print("Part 1:", score)

## Part 2:
# Calculate score for each game assuming second column is desired outcome
score = 0
for line in data:
    score += score_one_game_part2(line)
print("Part 2:", score)