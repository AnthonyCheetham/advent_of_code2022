# Day 11 of Advent of Code 2022

with open("datasets/day11_input.dat","r") as myf:
    data = myf.read()

# Monkeys throw items based on rules in the input
# Each item has a "worry level"
# Each round they inspect the items they have and throw them to other monkeys
# The monkey is chosen based on a True/False mathematical test

class Monkey(object):
    def __init__(self, input_strings):
        # Handle all of the complex string parsing in this init function
        item_string = input_strings[1]
        operation_string = input_strings[2]
        test_string = input_strings[3:]

        # Parse the item string
        items = item_string.split(":")[1].split(",")
        items = [int(i.strip()) for i in items]
        self.items = items
        
        # Parse the test string
        self.test_divisor = int(test_string[0].split(" ")[-1])
        self.test_monkey_true = int(test_string[1].split(" ")[-1])
        self.test_monkey_false = int(test_string[2].split(" ")[-1])

        # Process the operation string
        if "new = old * old" in operation_string:
            self.operation = lambda x: x * x
        elif "*" in operation_string:
            mult = int(operation_string.split(" ")[-1])
            self.operation = lambda x: x * mult
        elif "+" in operation_string:
            const = int(operation_string.split(" ")[-1])
            self.operation = lambda x: x + const
        else:
            print("Unknown operation:",operation_string)
        
        # Keep track of the number of items inspected
        self.n_inspections = 0
        # For part 2, add a modulo so the numbers dont get out of control
        self.mod = None
    
    def process_one_item(self):
        worry = self.items.pop(0)
        # Update worry level
        worry = self.operation(worry)
        # Switch for part 1 vs part 2
        if self.mod is None:
            worry = worry//3 # Part 1
        else:
            worry = worry % self.mod
        # Count it
        self.n_inspections += 1
        # Choose a recipient
        if (worry % self.test_divisor) == 0:
            recipient = self.test_monkey_true
        else:
            recipient = self.test_monkey_false
        return worry, recipient

def process_monkey(m, monkeys):
    while len(m.items) > 0:
        # Work out who to throw it to
        worry, recipient = m.process_one_item()
        # Throw it
        monkeys[recipient].items.append(worry)
        # print(f"Gave {worry} to {recipient}")

def one_round(monkeys):
    for m in monkeys:
        process_monkey(m, monkeys)

## Part 1:
# Set up the monkeys
monkey_strings = data.split("\n\n")
monkeys = []
for m in monkey_strings:
    monkeys.append(Monkey(m.splitlines()))

# Run n iterations
n = 20
for _ in range(n):
    one_round(monkeys)

# Find the "level of monkey business"
n_inspections = [m.n_inspections for m in monkeys]
n_inspections.sort()
print("Part 1:",n_inspections[-1]*n_inspections[-2])


## Part 2:
# Set up the monkeys again
monkeys_part2 = []
for m in monkey_strings:
    monkeys_part2.append(Monkey(m.splitlines()))
# To keep the numbers from overflowing, we can do mod of the multiple of 
# all the divisors, since a mod b is the same if you do (a mod (b*c)) first
big_mod = 1
for m in monkeys_part2:
    big_mod*= m.test_divisor
for m in monkeys_part2:
    m.mod = big_mod

# Run n iterations
n = 10000
for _ in range(n):
    one_round(monkeys_part2)

# Find the "level of monkey business"
n_inspections2 = [m.n_inspections for m in monkeys_part2]
n_inspections2.sort()
print("Part 2:",n_inspections2[-1]*n_inspections2[-2])