"""
Plotting functions
"""

# Globals
current_color = 0
plot_idx = 0

# Typing
from typing import List, Tuple, Literal

# Imports 
import os
import numpy as np
from matplotlib.figure import Figure
from matplotlib.axes import Axes
import matplotlib.pyplot as plt
from .program import Item
import plotwist as ptw 
import plotwist.program as ptp

# Make a temporary directory
def make_tmp_dir() -> None:
    """
    Make the tmp directory.
    """
    if not os.path.exists("tmp"):
        os.makedirs("tmp")
    if not os.path.exists("tmp/plots"):
        os.makedirs("tmp/plots", exist_ok=True)

# Add a plot to the html report
def add_fig() -> None:
    """
    Add the current figure to the html report.
    """
    global plot_idx
    make_tmp_dir()
    plt.savefig(f"tmp/plots/plot_{plot_idx}.svg")
    ptp.program.append(
        Item(
            f"<img src='plots/plot_{plot_idx}.svg'>"
        )
    )
    plot_idx += 1
    plt.clf()

# Context manager type instruction that embeds a subplot
class embedded_subplots:
    """
    Context manager type instruction that embeds a subplot 
    """
    def __init__(self, 
                 *args, 
                 embedding: Literal["plain", "scrollable", "interactive"] = "plain", 
                 **kwargs) -> None:
        """
        Initialize the embedded_subplots context manager.
        
        Args:
            *args: tuple: arguments for plt.subplots
            embedding: str: embedding type. Either "plain", "scrollable" or "interactive".
            **kwargs: dict: keyword arguments for plt.subplots
        """
        self.embedding = embedding
        self.fig, self.axs = plt.subplots(*args, **kwargs)

    def __enter__(self) -> Tuple[Figure, Axes]:
        return self.fig, self.axs
    
    def __exit__(self, *args) -> None:
        global plot_idx
        make_tmp_dir()
        if self.embedding == "plain":
            self.fig.savefig(f"tmp/plots/plot_{plot_idx}.svg")
            ptp.program.append(
                Item(
                    f"<img src='plots/plot_{plot_idx}.svg'>"
                )
            )
        elif self.embedding == "scrollable":
            self.fig.savefig(f"tmp/plots/plot_{plot_idx}.svg")
            ptp.program.append(
                Item(
                    f"<iframe src='plots/plot_{plot_idx}.svg' width='700px' height='500px'></iframe>"
                )
            )
        elif self.embedding == "interactive":
            import mpld3
            mpld3.save_html(self.fig, f"tmp/plots/plot_{plot_idx}.html")
            ptp.program.append(
                Item(
                    f"<iframe src='plots/plot_{plot_idx}.html' width='700px' height='500px'></iframe>"
                )
            )
        plot_idx += 1
        self.fig.clf()

class slider_subplots:
    """
    Context manager type instruction that embeds a subplot with a slider    
    """
    def __init__(self, n_plots: int, *args, embedding="plain", **kwargs) -> None:
        """
        Initialize the slider_subplots context manager.
        
        Args:
            n_plots: int: number of plots
            *args: tuple: arguments for plt.subplots
            embedding: str: embedding type. Either "plain", "scrollable" or "interactive".
            **kwargs: dict: keyword arguments for plt.subplots
        """
        self.embedding = embedding
        self.figs = []
        self.axs = []
        for i in range(n_plots):
            fig, ax = plt.subplots(*args, **kwargs)
            self.figs.append(fig)
            self.axs.append(ax)

    def __enter__(self) -> Tuple[List[Figure], 
                                 List[Axes]]:
        return self.figs, self.axs

    def __exit__(self, *args) -> None:
        global plot_idx
        make_tmp_dir()
        for fig in self.figs:
            if self.embedding == "interactive":
                import mpld3
                mpld3.save_html(fig, f"tmp/plots/plot_{plot_idx}.html")
            else:
                fig.savefig(f"tmp/plots/plot_{plot_idx}.svg")
            plot_idx += 1
        slider_plot_html = \
        f"""<span style="display: inline-flex; flex-direction: column;">
<input type="range" min="0" max="{len(self.figs) - 1}" value="0" class="slider" id="slider_{plot_idx}">
<{"img" if self.embedding == "plain" else "iframe"} src="plots/plot_{plot_idx - len(self.figs)}.{"html" if self.embedding == "interactive" else "svg"}" id="plot_{plot_idx}" {"width='700px' height='500px'" if not self.embedding == "plain" else ""}>{"</iframe>" if not self.embedding == "plain" else ""}
</span>"""
        script = \
f"""var slider_{plot_idx} = document.getElementById("slider_{plot_idx}");
var output_{plot_idx} = document.getElementById("plot_{plot_idx}");
slider_{plot_idx}.oninput = function() {{
    output_{plot_idx}.src = "plots/plot_" + ({plot_idx - len(self.figs)} + parseInt(this.value)) + ".{'html' if self.embedding == 'interactive' else 'svg'}";
}}"""

        ptp.program.append(
            Item(slider_plot_html, script=script)
        )
        plot_idx += 1
        for fig in self.figs:
            fig.clf()
