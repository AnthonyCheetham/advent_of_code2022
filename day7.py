# Day 7 of Advent of Code 2022

with open("datasets/day7_input.dat","r") as myf:
    data = myf.read() # Read it all in as a single string today

# Parse commands to turn it into a filesystem
# Will need to calculate sizes of directories, which are nested
# Plan: Make file and directory objects with recursive function

class FileObj(object):
    def __init__(self, size, name):
        self.size = size
        self.name = name

    def get_size(self):
        return self.size

class DirectoryObj(object):
    def __init__(self, parent, name):
        self.parent=parent
        if isinstance(self.parent, DirectoryObj):
            self.parent.add_child(self)
        self.children = [] # list of files and directories under this dir
        self.name = name
        self.size = None # For caching size of directory
    
    def add_child(self, child):
        self.children.append(child)

    def get_child(self, name):
        for c in self.children:
            if c.name == name:
                return c
    
    def get_size(self):
        if self.size is None:
            size = 0
            for c in self.children:
                size += c.get_size()
        else:
            size = self.size
        return size
    
    def size_of_children_under_limit(self, size_limit):
        """Function for Part 1.
        
        Find the total size of this directory + child directories,
        only counting those below size_limit.
        """
        # Check size of current dir
        dir_size = self.get_size()
        amount = 0
        if dir_size <= size_limit:
            amount += dir_size
        # And check children
        for child in self.children:
            if isinstance(child,DirectoryObj):
                amount += child.size_of_children_under_limit(size_limit)
        return amount

    def closest_to_size_minimum(self,size_min):
        """Function for Part 2.
        
        Comparing this directory and its child directories, find which one
        is closest to size_min, without going under.
        """
        dir_size = self.get_size()
        best_match_size = 9999999999999
        # If it's big enough, we can check child directories 
        if dir_size >= size_min:
            best_match_size = min(best_match_size, dir_size)

            for child in self.children:
                if isinstance(child,DirectoryObj):
                    child_size = child.closest_to_size_minimum(size_min)
                    if child_size >= size_min:
                        best_match_size = min(best_match_size, child_size)
        return best_match_size


    def __print__(self):
        return self.name

### Spend time once setting up the file system, then use it for both parts

# Start a directory for /
root_dir = DirectoryObj(None,"/")
current_dir = root_dir

# Since we read in the input as a string we can split commands by looking for $
commands_and_outputs = data.split("$")

# Loop through the commands and fill in the filesystem as we go
# Assume first line is $ cd /, which means the first entry in the list is blank
# and the second entry is just making "/", which we've already done
for c in commands_and_outputs[2:]:
    lines = c.splitlines()

    # The first line is the command
    command = lines[0].strip()
    output = lines[1:]

    if command == "cd ..":
        # Go back a directory
        current_dir = current_dir.parent
    elif command.startswith("cd"):
        # Go down a directory
        new_dir_name = command.split(" ")[1]
        # Find the directory if it exists
        new_dir = current_dir.get_child(new_dir_name)
        if not isinstance(new_dir, DirectoryObj):
            print("Directory not found:", new_dir_name)
            raise Exception("test")
        current_dir = new_dir

    elif command.startswith("ls"):
        # Make objects for all of the files and directories
        for f in output:
            type_amount, name = f.split(" ")
            
            if type_amount.isnumeric():
                # Then it's a file
                new_file = FileObj(int(type_amount),name)
                current_dir.add_child(new_file)
            elif type_amount == "dir":
                # Then it's a directory
                new_dir = DirectoryObj(current_dir, name)
            else:
                # Then I screwed up
                print("Unknown thing:",type_amount,name)
    else:
        print("Unknown command:",command)

## Part 1:
# Work out how many have a total size of at most 100000
# Then sum the sizes of those
print("Part 1:", root_dir.size_of_children_under_limit(100000))

## Part 2:
# What is the size of the directory that is closest to 30,000,000 
# (without going under)?
# How much do we need to delete
used_space = root_dir.get_size()
unused_space = 70000000 - used_space
to_delete = 30000000 - unused_space
print("Part 2:", root_dir.closest_to_size_minimum(to_delete))