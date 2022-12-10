# Day 10 of Advent of Code 2022

with open("datasets/day10_input.dat","r") as myf:
    data = myf.read().splitlines()

# CPU processing instructions.

class CPU(object):
    def __init__(self, instructions):
        self.register = 1
        self.cycle = 1
        self.register_record = []
        self.signal_strength = 0

        self.instructions = instructions
        self.screen = [["0" for x in range(40)] for y in range(6)]

    def one_cycle(self):
        """Process one cycle"""
        # Get next instruction
        inst = self.instructions.pop(0)
        
        if inst.startswith("noop"):
            # Do nothing
            pass
        elif inst.startswith("addx"):
            # First cycle nothing, then add
            # To simulate this, make a new instruction "nowaddx"
            # And add it to the start of the queue
            new_inst = "now"+inst
            self.instructions.insert(0,new_inst)
        elif inst.startswith("nowaddx"):
            amount = int(inst.split(" ")[-1])
            self.register += amount
        else:
            print("Unknown:",inst)
        
        # Update counter and record if necessary
        self.cycle += 1
        if (self.cycle % 40) == 20:
            self.register_record.append(self.register)
            self.signal_strength += self.cycle*self.register
        
    def run_all_instructions(self):
        while len(self.instructions) > 0:
            self.draw_pixel() # Part 2
            self.one_cycle()

    def draw_pixel(self):
        """For part 2. Draw pixel onto screen."""
        sym = "."
        xpos = (self.cycle-1) % 40
        ypos = (self.cycle-1)//40
        print(xpos,ypos)
        if abs(self.register - xpos) <= 1:
            sym = "#"
        self.screen[ypos][xpos] = sym
    
    def print_screen(self):
        for row in self.screen:
            print("".join(row))

# Part 1:
cpu = CPU(data)
cpu.run_all_instructions()
print("Part 1:",cpu.signal_strength)

# Part 2:
cpu.print_screen()