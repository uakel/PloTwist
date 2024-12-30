"""
Functions for regular reoccuring configurations of matplotlib axes.
"""
from typing import *
from matplotlib.ticker import FuncFormatter
from matplotlib.axes import Axes
import numpy as np

def format_large_numbers(range_: Tuple, x: float, pos: int) -> str:
    """
    Format large numbers in a human-readable way.
    
    Args:
        x: float: number to format
        pos: int: position

    Returns:
        str: formatted number
    """
    if abs(range_[1] - range_[0]) / abs(range_[0]) < 0.2:
        if range_[0] >= 1e12:
            offset = f'{range_[0]*1e-12:.1f}T'
        elif range_[0] >= 1e9:
            offset = f'{range_[0]*1e-9:.1f}B'
        elif range_[0] >= 1e6:
            offset = f'{range_[0]*1e-6:.1f}M'
        elif range_[0] >= 1e3:
            offset = f'{range_[0]*1e-3:.1f}K'
        elif range_[0] >= 1:
            offset = f'{range_[0]:.1f}'
        else:
            offset = f'{range_[0]:.3f}'

        delta = x - range_[0]
        if delta >= 1e12:
            d_exp = f'+{delta*1e-12:.1f}T'
        elif delta >= 1e9:
            d_exp = f'+{delta*1e-9:.1f}B'
        elif delta >= 1e6:
            d_exp = f'+{delta*1e-6:.1f}M'
        elif delta >= 1e3:
            d_exp = f'+{delta*1e-3:.1f}K'
        elif delta >= 1:
            d_exp = f'+{delta:.1f}'
        else:
            d_exp = f'+{delta:.3f}'

        if abs(x - range_[0]) / abs(range_[1] - range_[0]) < 0.15:
            return offset + d_exp
        return d_exp


    else:
        if x >= 1e12:
            return f'{x*1e-12:.1f}T'
        elif x >= 1e9:
            return f'{x*1e-9:.1f}B'
        elif x >= 1e6:
            return f'{x*1e-6:.1f}M'
        elif x >= 1e3:
            return f'{x*1e-3:.1f}K'
        elif x >= 1:
            return f'{x:.1f}'
        else:
            return f'{x:.3f}'

def decorate(ax: Axes, tick_label_offset: float = 0):
    """
    Decorate an axes with a grid and set the aspect ratio to be equal.
    """
    ax.grid(True)
    ax.legend()
    ax.get_xaxis().set_major_formatter(
        lambda x, pos: format_large_numbers(ax.get_xlim(), x, pos)
    )
    ax.get_yaxis().set_major_formatter(
        lambda x, pos: format_large_numbers(ax.get_ylim(), x, pos)
    )

C = ['#003049', '#d62828', '#f77f00', '#fcbf49', '#588157', '#3a5a40']
