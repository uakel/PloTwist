import numpy as np
from plotwist import *

# Insert titles and subtitles
title("Example Report")
# A rule can make your report more readable
rule()
subtitle("Embed interactive versions of your plots!")

# PloTwist works with context managers 
# that return axes that then get 
# automatically embedded in the report
with embedded_subplots(
    # The embedding argument selects the way the plots are displayed
    embedding="interactive" 
) as (fig, ax):
    x = np.linspace(0, 2 * np.pi, 100)
    ax.plot(x, np.sin(x), label='sin(x)')
    ax.plot(x, np.cos(x), label='cos(x)')
    ax.legend()
    ax.grid()

# Sliders are also supported!
subtitle("Even sliders are supported!")
with slider_subplots(19) as (figs, axs):
    for i, ax in enumerate(axs):
        x = np.linspace(0, 2 * np.pi, 100)
        ax.plot(x, np.sin(x + i * np.pi / 10), 
                label=f'sin(x + {i * np.pi / 10:0.2f})')
        ax.plot(x, np.cos(x) * i / 19,
                label=f'cos(x) * {i / 19:0.2f}') 
        ax.legend(loc='upper right')
        ax.grid()

# Changing the stacker makes the elements you
# add to the report appear at different positions
stacker("center")
subtitle("You can also change the layout of your report")
from matplotlib import pyplot as plt
x = np.linspace(0, 2 * np.pi, 100)
plt.plot(x, np.exp(-x) * np.cos(5 * x), label='exp(-x) * cos(5x)')
plt.legend()
plt.grid()
add_fig() # Plotting without context manager is 
          # also supported
# Add comments that allow others to understand
# your plots
comment("Note the nice standard template!")

# Trigger the report generation
make()

