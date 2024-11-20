import numpy as np
from plotwist import *

title("Example Report")
rule()
subtitle("Embed your Plots")
with embedded_subplots() as (fig, ax):
    x = np.linspace(0, 2 * np.pi, 100)
    ax.plot(x, np.sin(x), label='sin(x)')
    ax.plot(x, np.cos(x), label='cos(x)')
    ax.legend()
    ax.grid()

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

stacker("center")
subtitle("You can also change the layout of your report")
from matplotlib import pyplot as plt
x = np.linspace(0, 2 * np.pi, 100)
plt.plot(x, np.exp(-x) * np.cos(5 * x), label='exp(-x) * cos(5x)')
plt.legend()
plt.grid()
add_fig() # Plotting without context manager is 
          # also supported
comment("Note the nice standard template!")

make()

