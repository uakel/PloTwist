"""
PloTwist: A Python package for html report generation with minimal code.

Author: Leonard Franz
"""
# Use matplotlib style
from matplotlib import style
style.use(__file__.replace("__init__.py", "style.mplstyle"))

# Fill the namespace
from .instructions import *
from .plot import slider_subplots, embedded_subplots, add_fig
from .program import make
from .data_handling import make_nested_dict_from_sspe
from .logging import TimePrint
from .decorate import decorate, format_large_numbers, C 

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
    "make_nested_dict_from_sspe",
    "TimePrint",
    "decorate",
    "format_large_numbers",
    "C"
]
