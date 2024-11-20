"""
User accessible function (instructions)
that fill the program for the compiler.
"""

from .program import Item, ChangeStacker
import plotwist.program as ptp
from typing import Literal

# Item creating instructions
def title(title: str) -> None:
    """
    Add a title to the html report.

    Args:
        title: str, the title of the report

    Returns:
        None
    """
    # Make the HTML
    item = Item(f"<h1>{title}</h1>", mode="block")
    # Append the item to the program
    ptp.program.append(item)

def subtitle(subtitle: str) -> None:
    """
    Add a subtitle to the html report.

    Args:
        subtitle: str, the subtitle of the report

    Returns:
        None
    """
    # Make the HTML
    item = Item(f"<h2>{subtitle}</h2>", mode="block")
    # Append the item to the program
    ptp.program.append(item)

def comment(comment: str) -> None:
    """
    Add a comment to the html report.

    Args:
        comment: str, the comment

    Returns:
        None
    """
    # Make the HTML
    item = Item(f"<p>{comment}</p>", mode="block")
    # Append the item to the program
    ptp.program.append(item)

def rule() -> None:
    """
    Add a horizontal rule to the html report.

    Args:
        None

    Returns:
        None
    """
    # Make the HTML
    item = Item("<hr>", mode="block")
    # Append the item to the program
    ptp.program.append(item)

# Stackfluencer generating instructions
def stacker(stacker: Literal["normal", "center", "one", "two", "three", "four"]) -> None:
    """
    Change the stacker of the html report.

    Args:
        stacker: str, the stacker type
                 from either "normal",
                 "center", "one", "two",
                 "three", "four"


    Returns:
        None
    """
    # Make the stackfluencer
    stackfluencer = ChangeStacker(stacker)
    # Append the item to the program
    ptp.program.append(stackfluencer)
