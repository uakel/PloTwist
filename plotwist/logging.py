"""
A submodule with lots of helper functions for nice logging
"""

# Imports
from time import time

#############
# Constants #
#############

# Colors for the different levels
level_colors = ["\033[31m", "\033[32m", "\033[33m", "\033[34m", "\033[35m", "\033[36m"]
# Reset color string
reset_color = "\033[0m"

###########
# Globals #
###########

# Store how often the TimePrint class was entered
level = 0

###########
# Classes #
###########

class TimePrint:
    """
    Nice printing 'function' (context manager)that also 
    measures the time it takes to execute the below code block.
    """
    def __init__(self, message: str, nice=True) -> None:
        # Save the message
        self.message = message
        # Add decorations
        if nice:
            self.message = f"~~ {self.message} ~~"

    def __enter__(self) -> None:
        # Get the current color
        global level
        self.color = level_colors[level % len(level_colors)]
        # Print the message
        print(" " * 4 * level + self.color + self.message + reset_color)
        # Start the timer
        self.start = time()
        level += 1

    def _unit_map(self, dt: float) -> str:
        """
        Map a time in seconds to a human readable string.
        """
        if dt < 1e-6:
            return f"{dt * 1e9:.1f} ns"
        if dt < 1e-3:
            return f"{dt * 1e6:.1f} µs"
        if dt < 1:
            return f"{dt * 1e3:.1f} ms"
        if dt < 60:
            return f"{dt:.1f} s"
        if dt < 3600:
            return f"{dt / 60:.1f} min"
        return f"{dt / 3600:.1f} h"

    def __exit__(self, *args):
        # Print the time it took
        dt = time() - self.start
        print(self.color + f"done ({self._unit_map(dt)})" + reset_color)
        # Decrese the current level
        global level
        level -= 1
