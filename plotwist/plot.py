"""
Plotting functions
"""

# Globals
current_color = 0
plot_idx = 0

# Typing
from typing import Dict, Callable, List, Tuple, Any

# Imports 
import numpy as np
from matplotlib.figure import Figure
from matplotlib.axes import Axes
import matplotlib.pyplot as plt
from .program import Item
import plotwist as ptw 

# Context manager type instruction that embeds a subplot
class embedded_subplots:
    def __init__(self, *args, **kwargs) -> None:
        self.fig, self.axs = plt.subplots(*args, **kwargs)

    def __enter__(self) -> Tuple[Figure, Axes]:
        return self.fig, self.axs
    
    def __exit__(self, *args) -> None:
        global plot_idx
        self.fig.savefig(f"report/plots/plot_{plot_idx}.svg")
        ptw.program.append(Item(
            f"<img src='plots/plot_{plot_idx}.svg'>")
        )
        plot_idx += 1

###############
# Legacy code #
###############

# Constants
COLORS =["#003049", "#d62828", "#f77f00", "#fcbf49", "#eae2b7"]

# Formatting
from .data_handling import NestedDict
from .processing import moving_average
from matplotlib.ticker import FuncFormatter

def format_large_numbers(x: float, pos: int) -> str:
    """
    Format large numbers in a human-readable way.
    
    Args:
        x: float: number to format
        pos: int: position

    Returns:
        str: formatted number
    """
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
        return f'{x:.2f}'

# Plot functions
def type_one_plot(x: np.ndarray,
                  y: np.ndarray,
                  ax: plt.Axes,
                  n: int = 1,
                  label: str = "",
                  stds: np.ndarray | None = None):
    """
    Plot a moving average of a signal
    with raw data points and smoothed
    standard deviations.

    Args:
        x: np.ndarray, x-axis values
        y: np.ndarray, y-axis values
        ax: plt.Axes, axis to plot on
        n: int, window size
        label: str, label for the plot
        stds: np.ndarray, standard deviations

    Returns:
        None
    """
    # Plot the raw data with the current color
    global current_color
    ax.plot(x, y, ".", 
            alpha=0.5,
            color=COLORS[current_color])
    # Calculate the moving average
    average = moving_average(y, n)

    # Plot the moving average
    ax.plot(np.array(x),
            average, 
            color=COLORS[current_color], 
            lw=2.5,
            label=label)

    # Plot the smoothed standard deviations
    # around the moving average if given
    if stds is not None:
        stds = moving_average(stds, n)
        stds = np.array(stds)
        ax.fill_between(x, 
                        average - stds,
                        average + stds,
                        color=COLORS[current_color],
                        alpha=0.4)

    # Update the colors
    current_color = (current_color + 1) % len(COLORS)
    ax.set_xlim((x[0], x[-1]))

# Item creators
def plot(*args, **kwargs):
    """
    Create a plot and save it to the report.
    """
    fig, ax = plt.subplots()
    ax.plot(*args, **kwargs)
    global plot_idx
    fig.savefig(f"report/plots/plot_{plot_idx}.svg")
    ptw.program.append(Item(
        f"<img src='plots/plot_{plot_idx}.svg'>")
    )
    plot_idx += 1

# Specialized plot functions
# for tree-like data containers
# given by a dict of dicts
def type_one_comparative(data: Dict[str, Dict | Any],
                         x: str,
                         ys: List[str],
                         stds: List[str] | None = None,
                         x_transform: Callable = lambda x: x,
                         y_transform: Callable = lambda y: y,
                         x_label: str = "x",
                         y_label: str = "y",
                         title: str = "Plot"):
    """
    Create a comparative plot of multiple smoothed 
    signals with moving averages and standard deviations 
    from the key paths in the data dictionary.

    Args:
        data: dict of dicts representing a tree
              where the leaves are data and the 
              tree defines paths to the data
        x: str, x-axis key path
        y: list, y-axis key paths
        stds: list, standard deviation key paths
        x_transform: lambda, x-axis transformation
                     (is applied before plotting)
        y_transform: lambda, y-axis transformation
                      (is applied before plotting)
        xl: str, x-axis label
        yl: str, y-axis label
        title: str, title
    """
    # Create a new figure
    fig, ax = plt.subplots()
    # Set the x-axis and y-axis formatters
    ax.xaxis.set_major_formatter(
        FuncFormatter(format_large_numbers)
    )
    ax.yaxis.set_major_formatter(
        FuncFormatter(format_large_numbers)
    )

    # Cast the data to a nested dictionary
    wrapped_data = NestedDict(data)

    std_list = stds if stds else [None] * len(ys)
    for y, s in zip(ys, std_list):
        x_data = x_transform(wrapped_data[x])
        y_data = y_transform(wrapped_data[y])
        stdsd = wrapped_data[s] if s else None
        type_one_plot(x_data, y_data, ax, label=y, stds=stdsd)

    ax.set_xlabel(x_label)
    ax.set_ylabel(y_label)
    ax.set_title(title)
    ax.legend()
    ax.grid(alpha=0.3)
    ax.tick_params(axis='x', which='major')
    global current_color
    current_color = 0
    global plot_idx
    fig.savefig(f"report/plots/plot_{plot_idx}.svg")
    ptw.program.append(Item(
        f"<img src='plots/plot_{plot_idx}.svg'>")
    )
    plot_idx += 1

def density_from_percentiles(data: Dict[str, Dict | Any],
                             x: str,
                             y: str,
                             percentile_keys: List[str] = ["min"] + 
                                 [f"p{i}"for i in range(10, 100, 10)] + ["max"],
                             title: str = "Density plot",
                             ) -> None:
    """
    Create a density plot from percentiles.

    Args:
        data: dict of dicts representing a tree
              where the leaves are data and the 
              tree defines paths to the data
        x: str, x-axis key path
        y: str, y-axis key path
        percentile_keys: list, percentile subkeys
        title: str, title

    Returns:
        None
    """

    def color(density: float, r: Tuple[float, float]=(0, 1)) -> Tuple[float, float, float]:
        """
        Determine the color of the density.

        Args:
            density: float, density
            r: tuple, range

        Returns:
            str: color
        """
        score = (density - r[0]) / (r[1] - r[0])
        score = max(0, min(1, score))
        return (1 - score * 0.7, 1 - score * 0.7, 1 - score * 0.7)

    # Create a new figure
    fig, ax = plt.subplots()
    # Set the x-axis and y-axis formatters
    ax.xaxis.set_major_formatter(
        FuncFormatter(format_large_numbers)
    )
    ax.yaxis.set_major_formatter(
        FuncFormatter(format_large_numbers)
    )
    ax.set_xlabel(x)
    ax.set_ylabel(y)
    ax.set_title(title)

    # Cast the data to a nested dictionary
    wrapped_data = NestedDict(data)
    xp = wrapped_data[x]
    y_data = wrapped_data[y]

    # Plot the density
    max_density = [max(1 / (1.01 * y_data[next_key][i] - y_data[key][i])
                   for key, next_key in zip(percentile_keys[:-1], percentile_keys[1:])) 
                   for i in range(len(xp))]
    for i, (key, next_key) in enumerate(zip(percentile_keys[:-1], percentile_keys[1:])):
        y = y_data[key]
        next_y = y_data[next_key]
        for j, (y_val, next_y_val) in enumerate(zip(y, next_y)):
            density = 1 / (1.01 * next_y_val - y_val) 
            ax.bar([xp[j]], [next_y_val - y_val], bottom=[y_val], 
                   color=color(density, (0, max_density[j])),
                   align="edge", width=xp[j + 1] - xp[j] 
                   if j < len(xp) - 1 else xp[j] - xp[j - 1],
                   edgecolor="black", linewidth=0.4)
    ax.set_xlim((xp[0], xp[-1] + (xp[-1] - xp[-2])))
    ax.set_ylim((min(y_data["min"]), max(y_data["max"])))
    ax.grid(alpha=0.3, color="black", linestyle="--")
    global current_color
    current_color = 0
    global plot_idx
    fig.savefig(f"report/plots/plot_{plot_idx}.svg")
    ptw.program.append(Item(
        f"<img src='plots/plot_{plot_idx}.svg'>")
    )
    plot_idx += 1

def nth_listvalued_of_all_subkeys(data: Dict,
                                  key: str,
                                  n: int,
                                  title: str = "Plot",
                                  subsubkey_max: int = 5,
                                  comparator: List[List[float]] | None = None,
                                  labels: List[str] | None = None) -> None:
    """
    Make a plot for all subkeys with the nth list of each subsubkey.

    Args:
        data: dict of dicts representing a tree
              where the leaves are data and the 
              tree defines paths to the data
        key: str, key path. Must point to a dictionary
             where all keys point to lists of lists
        n: int, index of the list to plot in each subsubkey
        title: str, title. Default is "Plot"
        subsubkey_max: int, maximum number of subsubkeys to plot.
                       The selected subsubkeys are randomly chosen.
        comparator: list of lists of floats. If the comparator 
                    is given, the lists are plotted allongside the
                    subsubkeys for each subkey.

    Returns:
        None
    """
    # Cast the data to a nested dictionary
    wrapped_data = NestedDict(data)[key]
    subkeys = list(wrapped_data.dictionary.keys())
    try:
        subkeys = sorted(subkeys, key=lambda x: int(x))
    except ValueError:
        pass

    # Create a new figure
    fig, axs = plt.subplots(len(subkeys), 1, figsize=(7, len(subkeys) + 2))
    plt.subplots_adjust(hspace=0.1, bottom=1/(len(subkeys) + 2), top=1-1/(len(subkeys) + 2))
    fig.suptitle(title, x=0.5, y=1 - 1/(len(subkeys) + 2) / 2)

    # Set the x-axis and y-axis formatters
    for ax in axs:
        ax.xaxis.set_major_formatter(
            FuncFormatter(format_large_numbers)
        )
        ax.yaxis.set_major_formatter(
            FuncFormatter(format_large_numbers)
        )

    for j, (subkey, ax) in enumerate(zip(subkeys, axs)):
        subsubkeys = wrapped_data[subkey].dictionary.keys()

        max_len = 0
        for i, subsubkey in enumerate(subsubkeys):
            if i >= subsubkey_max:
                break
            last_list = wrapped_data[subkey][subsubkey][n]
            max_len = max(max_len, len(last_list))
            x = np.arange(len(last_list) - 1)
            # if comparator is not None:
            #     best_shift, score = find_best_shift(last_list, comparator[j], 100)
            #     x += best_shift
            ax.plot(x, last_list[:-1], color=COLORS[0], alpha=0.5)
        if comparator is not None:
            ax.plot(comparator[j], color=COLORS[1], label="Comparator")
        if labels is not None:
            ax.set_ylabel(labels[j])
        else:
            ax.set_ylabel(subkey)
        ax.grid(alpha=0.3)
        ax.set_xlim((0, max_len))
        if j == len(subkeys) - 1:
            ax.set_xlabel("Time")
        else:
            ax.set_xticklabels([])
    
    global current_color
    current_color = 0
    global plot_idx
    fig.savefig(f"report/plots/plot_{plot_idx}.svg")
    ptw.program.append(Item(
        f"<iframe src='plots/plot_{plot_idx}.svg' width='700px' height='500px'></iframe>")   
    )
    plot_idx += 1
