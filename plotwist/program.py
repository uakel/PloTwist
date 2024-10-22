"""
Programming Elements
"""
# Imports
from abc import ABC, abstractmethod
from .constants import HEADER

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
        self.html += "</body>\n</html>"

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
    def __init__(self, html, mode="inline"):
        self.html = html
        self.mode = mode

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
