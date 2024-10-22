"""
PloTwist: A Python package for html report generation from 
          semicolon separated python expression files (.sspe) 
          with minimal code.

Author: Leonard Franz
"""
# Typing
from typing import List

# Imports
import os
from . import program as pm

# Global variables
program: List[pm.Item | pm.Stackfluencer] = []

# Functions
def make():
    stacker: pm.Stacker = pm.NormalStacker()
    for instruction in program:
        if issubclass(type(instruction), pm.Item):
            stacker.stack(instruction)
        elif issubclass(type(instruction), pm.Stackfluencer):
            stacker = instruction.influence(stacker)
        else:
            raise ValueError("Unknown instruction type.")
    stacker.end()
    with open("report/index.html", "w") as file:
        file.write(stacker.html)
    program.clear()
        

# Make folder structure
os.makedirs("report", exist_ok=True)
os.makedirs("report/plots", exist_ok=True)

# Fill the namespace
from .data_handling import make_dict_from_sspe
from .plot import type_one_comparative
from .program import ChangeStacker
