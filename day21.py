# Day 21 of Advent of Code 2022

with open("datasets/day21_input.dat","r") as myf:
    data = myf.read().splitlines()

# Each line is a monkey that either performs a math operation using values 
# from other monkeys or has a number

class Monkey(object):
    def __init__(self,line,monkeys_list):
        name, eqn = line.split(":")
        self.name = name
        self.eqn = eqn.strip()
        self.num = None
        self.parse_eqn(self.eqn)

        self.monkeys = monkeys_list

    def parse_eqn(self,eqn):
        if eqn.isnumeric():
            self.num = int(eqn)
        else:
            self.eqn_vals = eqn.strip().split(" ")
    
    def value(self):
        if self.num is not None:
            return self.num
        else:
            m1,operation,m2 = self.eqn_vals
            if operation == "+":
                num = self.monkeys[m1].value() + self.monkeys[m2].value()
            elif operation == "-":
                num = self.monkeys[m1].value() - self.monkeys[m2].value()
            elif operation == "*":
                num = self.monkeys[m1].value() * self.monkeys[m2].value()
            elif operation == "/":
                num = self.monkeys[m1].value() // self.monkeys[m2].value()
            elif operation == "==":
                num = self.monkeys[m1].value() - self.monkeys[m2].value()
            # Save time by caching this (assuming it never needs recalculating)
            # if self.monkeys[m1].num is not None and self.monkeys[m2].num is not None and m1 != "humn" and m2 != "humn":
                # self.num = num
            # self.num = num # Save for next time
            return num

monkeys = {}
for line in data:
    m = Monkey(line,monkeys)
    monkeys[m.name] = m
print("Part 1:",monkeys["root"].value())

## For Part 2:
## Actually the equation for root should be "==" 
## And the line humn is an unknown input
## Find the value for humn that gives True for root

# Update the input
for ix,line in enumerate(data):
    line = data[ix]
    if line.startswith("root"):
        data[ix] = line.replace("+","==")
    elif line.startswith("humn"):
        humn_ix = ix

monkeys = {}
for ix,line in enumerate(data):
    m = Monkey(line,monkeys)
    monkeys[m.name] = m

# The equation has to be a polynomial since it's all +-*/
# Maybe we can do a quick gradient descent?
def f(monkeys,x):
    monkeys["humn"].num = x
    res = monkeys["root"].value()
    return res

# Start value
last_x = 0
last_y = f(monkeys,last_x)
l = 0.8 # learning rate / step size scaling

# Did some guess and check here because there are multiple values that solve the eqn
# But only one of them was accepted by advent of code. (maybe because of rounding?)
x = 1000
for ix in range(100):
    y = f(monkeys,x)
    if y == 0:
        val = x
        break
    grad = (y-last_y)/(x-last_x)

    # Update
    last_x = x
    last_y = y
    x = int(last_x - l*last_y/grad)

print("Part 2:",val)