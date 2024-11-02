"""
Programming Elements
"""
# Imports
from abc import ABC, abstractmethod
from .constants import HEADER
from typing import List

############################
# Stackers (Compile Modes) #
############################

# Base class
class Stacker(ABC):
    """
    A class for stacking items in the html report.
    """
    def __init__(self):
        self.html = "<html>\n"
        self.script = "<script>\n"

    @abstractmethod
    def stack(self, item):
        """
        Stacks the item in the html report.
        """

    @abstractmethod
    def close(self):
        """
        Closes the stacker.
        """

    def end(self):
        """
        Ends the html report.
        """
        self.close()
        self.script += "</script>\n"
        self.html += "</body>\n" + self.script + "</html>"

# Sub classes
class NormalStacker(Stacker):
    """
    A class for stacking items in the html report.
    """
    def __init__(self):
        super().__init__()
        self.html += HEADER
        self.html += "<body>\n"

    def stack(self, item):
        """
        Stacks the items in the html report.
        """
        self.html += item.html + "\n"
        if item.script != "":
            self.script += item.script + "\n"

    def close(self):
        """
        Closes the stacker.
        """
        pass

class ColumnStacker(Stacker):
    """
    A class for stacking items in the html report.
    """
    def __init__(self, columns: int):
        super().__init__()
        self.html += HEADER
        self.html += "<body>\n"
        self.column = 0
        self.columns = columns

    def stack(self, item):
        """
        Stacks the items in the html report.
        """
        if item.script != "":
            self.script += item.script + "\n"
        if item.mode == "block":
            self.html += item.html + "<br>"
            self.column = 0
        else:
            self.html += item.html
            self.column += 1
            if self.column == self.columns:
                self.html += "<br>"
                self.column = 0
        self.html += "\n"

    def close(self):
        """
        Closes the stacker.
        """
        pass

class CenterStacker(Stacker):
    """
    A class for stacking items in the html report.
    """
    def __init__(self):
        super().__init__()
        self.html += HEADER
        self.html += "<body>\n"

    def stack(self, item):
        """
        Stacks the items in the html report.
        """
        if item.script != "":
            self.script += item.script + "\n"
        self.html += f"<center>{item.html}</center><br>\n"

    def close(self):
        """
        Closes the stacker.
        """
        pass

#########################
# Compiler Instructions #
#########################

# Base Instructions
class Item:
    """
    A class for an item in the html report.
    """
    def __init__(self, html, mode="inline", script=""):
        self.html = html
        self.mode = mode
        self.script = script

class Stackfluencer(ABC):
    """
    Influences the current stacker
    """
    @abstractmethod
    def influence(self, stacker: Stacker) -> Stacker:
        """
        Influences the current stacker
        """

# Special case Instructions
class ChangeStacker(Stackfluencer):
    """
    A class for changing the stacker
    """
    def __init__(self, stacker: str):
        if stacker == "normal":
            self.stacker = NormalStacker()
        elif stacker == "one":
            self.stacker = ColumnStacker(1)
        elif stacker == "two":
            self.stacker = ColumnStacker(2)
        elif stacker == "three":
            self.stacker = ColumnStacker(3)
        elif stacker == "four":
            self.stacker = ColumnStacker(4)
        elif stacker == "center":
            self.stacker = CenterStacker()
        else:
            raise ValueError("Unknown stacker type.")

    def influence(self, stacker: Stacker) -> Stacker:
        """
        Influences the current stacker
        """
        stacker.close()
        self.stacker.html = stacker.html
        return self.stacker

# Program for the compiler
program: List[Item | Stackfluencer] = []

# Compiler
def make():
    # Initialize a NormalStacker
    stacker: Stacker = NormalStacker()
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
