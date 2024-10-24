"""
PloTwist: A Python package for html report generation with minimal code.

Author: Leonard Franz
"""
# Typing
from typing import List

# Imports
import os
from .program import Item, Stackfluencer, NormalStacker

# Program for the compiler
program: List[Item | Stackfluencer] = []

# Make folder structure
os.makedirs("report", exist_ok=True)
os.makedirs("report/plots", exist_ok=True)

# Compiler
def make():
    # Initialize a NormalStacker
    stacker: Stacker =NormalStacker()
    # Let the stacker compile the program
    for instruction in program:
        # If the instruction is an Item
        # let the stacker stack it
        if issubclass(type(instruction), Item):
            stacker.stack(instruction)
        # If the instruction is a Stackfluencer
        # influence the stacker
        elif issubclass(type(instruction), Stackfluencer):
            stacker = instruction.influence(stacker)
        # If the instruction is neither an Item
        # nor a Stackfluencer, then the Program
        # is invalid.
        else:
            raise ValueError("Unknown instruction type.")
    # Tell the stacker that no more items are coming
    stacker.end()
    # Write the html to a file
    with open("report/index.html", "w") as file:
        file.write(stacker.html)
    # Clear the program
    program.clear()
