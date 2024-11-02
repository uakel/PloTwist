"""
PloTwist: A Python package for html report generation with minimal code.

Author: Leonard Franz
"""
# Use matplotlib style
from matplotlib import style
style.use(__file__.replace("__init__.py", "style.mplstyle"))

# Imports
import os

# Make folder structure
os.makedirs("report", exist_ok=True)
os.makedirs("report/plots", exist_ok=True)

# Fill the namespace
from .instructions import *
from .plot import slider_subplots, embedded_subplots, add_fig
from .program import make

# __all__ variable
__all__ = [
    "title",
    "subtitle", 
    "comment",
    "rule",
    "stacker",
    "make",
    "add_fig",
    "slider_subplots",
    "embedded_subplots",
]
